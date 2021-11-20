from pydantic import BaseModel
from typing import Optional

from sqlalchemy.sql.sqltypes import DateTime

class PaketTable(BaseModel):  
    kodePaket: str
    tanggal: Optional[DateTime] = None
    deskripsi: Optional[str] = None