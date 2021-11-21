from sqlalchemy import Column, Integer, String
from db import Base
from db import ENGINE


# Bikin class model
class SoalTable(Base):
    __tablename__ = 'soal'
    id = Column(Integer, primary_key=True, autoincrement=True)
    kodeSoal = Column(Integer, nullable=False)
    pertanyaan = Column(String(255))
    pilihanJawaban = Column(String(255))
    kunciJawaban = Column(String(255))
    kodePaket = Column(String(30), nullable=False)

def main():
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()
