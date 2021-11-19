from sqlalchemy import Column, Integer, String
from db import Base
from db import ENGINE


# Bikin class model
class SoalTable(Base):
    __tablename__ = 'soal'
    kodeSoal = Column(Integer, primary_key=True, nullable=False)
    pertanyaan = Column(String(256))
    pilihanJawaban = Column(String(256))
    kunciJawaban = Column(String)
    kodePaket = Column(String(16), nullable=False)

def main():
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()
