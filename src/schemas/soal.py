from pydantic import BaseModel
from typing import Optional

class Soal(BaseModel):  # User Auth
    kodeSoal: int
    pertanyaan: str
    pilihanJawaban: str
    kunciJawaban: str
    kodePaket: str