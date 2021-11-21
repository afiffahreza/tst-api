from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.sql.expression import false 
from starlette.middleware.cors import CORSMiddleware
from db import session  
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from models.user import UserTable
from schemas.jawaban import Jawaban
from schemas.pembelian import Pembelian
from schemas.user import *
from schemas.hasil import *
from schemas.paket import *
from schemas.soal import *
from models.soal import SoalTable
from models.jawaban import JawabanTable
from models.hasil import HasilTable
from models.paket import PaketTable
from models.pembelian import PembelianTable

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

@app.get("/")
async def root():
    return {"message": "go to /docs for full API endpoints"}

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


@app.get("/users/me/")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    userme = session.query(UserTable).\
        filter(UserTable.username == current_user.username).first()
    return userme


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
async def create_soal(soal: Soal, current_user: User = Depends(get_current_active_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    newSoal = soal.dict()
    soalData = SoalTable()
    soalData.kodeSoal=newSoal['kodeSoal']
    soalData.pertanyaan=newSoal['pertanyaan']
    soalData.pilihanJawaban=newSoal['pilihanJawaban']
    soalData.kunciJawaban=newSoal['kunciJawaban']
    soalData.kodePaket=newSoal['kodePaket']
    session.add(soalData)
    session.commit()
    if soalData:
        return newSoal
    raise HTTPException(status_code=400, detail=f'Bad request')

@app.delete('/soal/{kodePaket}/{kodeSoal}')
async def delete_soal(kodeSoal: int, kodePaket: str, current_user: User = Depends(get_current_active_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    soalData = session.query(SoalTable).\
        filter(SoalTable.kodePaket == kodePaket and SoalTable.kodeSoal == kodeSoal).first()
    if soalData:
        session.query(SoalTable).filter(SoalTable.kodePaket == kodePaket and SoalTable.kodeSoal == kodeSoal).delete()
        session.commit()
        return soalData
    raise HTTPException(status_code=400, detail=f'Bad request')

#retrieve soal based on kodePaket
@app.get('/soal/{kodePaket}')
async def read_soal(kodePaket:str, current_user: User = Depends(get_current_active_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    soal = session.query(SoalTable).\
        filter(SoalTable.kodePaket == kodePaket).all()
    return soal

#masukin jawaban ke database
@app.post('/jawaban')
async def create_jawaban(jawaban: Jawaban, current_user: User = Depends(get_current_active_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    newJawaban = jawaban.dict()
    jawabanData = JawabanTable()
    jawabanData.username=newJawaban['username']
    jawabanData.kodePaket=newJawaban['kodePaket']
    jawabanData.kodeSoal=newJawaban['kodeSoal']
    jawabanData.jawaban=newJawaban['jawaban']
    session.add(jawabanData)
    session.commit()
    if jawabanData:
        return newJawaban
    raise HTTPException(status_code=400, detail=f'Bad request')

#retrieve jawaban based on kodeSoal
@app.get('/jawaban/{kodeSoal}')
async def read_jawaban(kodeSoal:int, current_user: User = Depends(get_current_active_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    jawaban = session.query(JawabanTable).\
        filter(JawabanTable.kodeSoal == kodeSoal).all()
    return jawaban

# Get hasil to diri sendiri by paketSoal
@app.get("/hasil/me/{paket_id}")
async def read_hasil_by_kodePaket(paket_id: str, current_user: User = Depends(get_current_active_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    paket = session.query(HasilTable).\
        filter(HasilTable.kodePaket == paket_id and HasilTable.username == current_user.username).first()
    return paket

# Post hasil TO diri sendiri based on paketSoal
@app.post("/hasil", response_model=User)
async def create_hasil(hasil: HasilCreate, current_user: User = Depends(get_current_active_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    newHasil = hasil.dict()
    hasilData = HasilTable()
    hasilData.username = newHasil['username']
    hasilData.kodePaket = newHasil['kodePaket']
    hasilData.nilai = newHasil['nilai']
    hasilData.ranking = newHasil['nilai']
    session.add(hasilData)
    session.commit()
    if hasilData:
        return newHasil
    raise HTTPException(status_code=400, detail=f'Bad request')
    
# Get hasil TO diri sendiri based on paketSoal
@app.get("/hasil/me/{paket_id}")
async def read_hasil_by_kodePaket(paket_id: str, current_user: User = Depends(get_current_active_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    paket = session.query(HasilTable).\
        filter(HasilTable.username == User.username and
               HasilTable.kodePaket == paket_id).first()
    return paket

# Post paket baru
@app.post("/paket")
async def create_paket(paket: PaketCreate, current_user: User = Depends(get_current_active_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    newPaket = paket.dict()
    paketData = PaketTable()
    paketData.kodePaket = newPaket['kodePaket']
    paketData.tanggal = newPaket['tanggal']
    paketData.deskripsi = newPaket['deskripsi']
    session.add(paketData)
    session.commit()
    if paketData:
        return newPaket
    raise HTTPException(status_code=400, detail=f'Bad request')
    
# Get paket all
@app.get("/paket")
async def read_paket(current_user: User = Depends(get_current_active_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    paket = session.query(PaketTable).all()
    return paket

# Get paket based paket_id
@app.get("/paket/{paket_id}")
async def read_paket(kode_paket: str, current_user: User = Depends(get_current_active_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    paket = session.query(PaketTable).\
        filter(PaketTable.kodePaket == kode_paket).first()
    return paket

# Get paket based paket_id
@app.delete("/paket/{paket_id}")
async def delete_paket(kode_paket: str, current_user: User = Depends(get_current_active_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    paket = session.query(PaketTable).\
        filter(PaketTable.kodePaket == kode_paket).first()
    if paket:
        session.query(PaketTable).filter(PaketTable.kodePaket == kode_paket).delete()
        session.commit()
        return paket
    raise HTTPException(status_code=400, detail=f'Bad request')

@app.get("/pembelian/{username}")
async def read_pembelian(username: str, current_user: User = Depends(get_current_active_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    pembelian = session.query(PembelianTable).\
        filter(PembelianTable.username == username).all()
    return pembelian

@app.post("/pembelian")
async def create_pembelian(pembelian: Pembelian, current_user: User = Depends(get_current_active_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    newPembelian = pembelian.dict()
    pembelianData = PembelianTable()
    pembelianData.kodePaket = newPembelian['kodePaket']
    pembelianData.username = newPembelian['username']
    session.add(pembelianData)
    session.commit()
    if pembelianData:
        return newPembelian
    raise HTTPException(status_code=400, detail=f'Bad request')