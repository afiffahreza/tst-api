from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):  # Token class
    access_token: str
    token_type: str


class TokenData(BaseModel):  # Token class
    username: Optional[str] = None


class User(BaseModel):  # User Auth
    username: str
    email: Optional[str] = None
    name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):  # User Auth
    hashed_password: str


class UserCreate(BaseModel):  # User Auth
    username: str
    password: str
    email: Optional[str] = None
    name: Optional[str] = None