from pydantic import BaseModel
from typing import Optional

class HasilTable(BaseModel):  
    username: str
    kodePaket: str
    nilai: Optional[int] = None
    ranking: Optional[int] = None

class HasilCreate(BaseModel):  # User Auth
    username: str
    kodePaket: str
    nilai: Optional[int] = None
    ranking: Optional[int] = None