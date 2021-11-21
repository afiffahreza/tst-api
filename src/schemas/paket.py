from pydantic import BaseModel
from typing import Optional


class PaketCreate(BaseModel):  # User Auth
    kodePaket: str
    tanggal: Optional[str] = None
    deskripsi: Optional[str] = None