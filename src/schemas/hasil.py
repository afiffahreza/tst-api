from pydantic import BaseModel
from typing import Optional

class HasilCreate(BaseModel):  # User Auth
    username: str
    kodePaket: str
    nilai: Optional[int] = None
    ranking: Optional[int] = None