from pydantic import BaseModel
from typing import Optional

class Jawaban(BaseModel):  # User Auth
    username: str
    kodePaket: str
    kodeSoal: int
    jawaban: str