from logging import FATAL
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.sql.expression import false 
from starlette.middleware.cors import CORSMiddleware
from db import session  
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from models.user import UserTable
from schemas.user import *
from src.db import conn
from models.soal import soal
from models.jawaban import jawaban


# secret key string from openssl rand -hex 32
SECRET_KEY = "02b55af9a51f87aea76b6406f5667f1341985add1c527afcbd2fcabb46318ab3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    user = session.query(UserTable).\
        filter(UserTable.username == username).first()
    if user:
        return user


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    users = session.query(UserTable).all()
    user = get_user(users, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    users = session.query(UserTable).all()
    user = authenticate_user(
        users, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/register", response_model=User)
async def register(user: UserCreate):
    newUser = user.dict()
    userData = UserTable()
    userData.username = newUser['username']
    userData.name = newUser['name']
    userData.email = newUser['email']
    userData.hashed_password = get_password_hash(newUser['password'])
    userData.disabled = 0
    session.add(userData)
    session.commit()
    if userData:
        return newUser
    raise HTTPException(status_code=400, detail=f'Bad request')


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users")
async def read_users(current_user: User = Depends(get_current_active_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    users = session.query(UserTable).all()
    return users

@app.get("/users/id/{user_id}")
async def read_user_by_id(user_id: int, current_user: User = Depends(get_current_active_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    user = session.query(UserTable).\
        filter(UserTable.id == user_id).first()
    return user

@app.get("/users/{username}")
async def read_user_by_username(username: str, current_user: User = Depends(get_current_active_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    user = session.query(UserTable).\
        filter(UserTable.username == username).first()
    return user

#masukin soal ke database
@app.post('/soal')
async def write_soal(kodeSoal:int, current_user: User = Depends(get_current_active_user)):
    return conn.execute(soal.insert().values(
        kodeSoal=soal.kodeSoal,
        pertanyaan=soal.pertanyaan,
        pilihanJawaban=soal.pilihanJawaban,
        kunciJawaban=soal.kunciJawaban,
        kodePaket=soal.kodePaket
    )).fetchall()

#retrieve soal based on kodePaket
@app.get('/soal/{kodePaket}')
async def read_soal(kodePaket:str, current_user: User = Depends(get_current_active_user)):
    return conn.execute(soal.select().where(soal.c.kodePaket == kodePaket)).fetchall

#masukin jawaban ke database
@app.post('jawaban')
async def write_jawaban(kodeSoal:int, username:str, current_user: User = Depends(get_current_active_user)):
    return conn.execute(jawaban.insert().values(
        username=jawaban.username,
        kodePaket=jawaban.kodePaket,
        kodeSoal=jawaban.kodeSoal,
        jawaban=jawaban.jawaban,
    )).fetchall()

#retrieve kunci jawaban dari soal based on kodeSoal
#@app.get('/jawaban/soal/{kodeSoal}')
#async def read_kunci(kodeSoal:int, current_user: User = Depends(get_current_active_user)):
    #

#retrieve jawaban based on kodeSoal
@app.get('/jawaban/{kodeSoal}')
async def read_jawaban(kodeSoal:int, username:str, current_user: User = Depends(get_current_active_user)):
    return conn.execute(jawaban.select().where(jawaban.c.kodeSoal == kodeSoal)).fetchall
