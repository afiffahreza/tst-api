from pydantic import BaseModel
from typing import Optional


class Pembelian(BaseModel):  
    username: str
    kodePaket: str