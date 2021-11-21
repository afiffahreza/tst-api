from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import DateTime
from db import Base
from db import ENGINE


class PaketTable(Base):
    __tablename__ = 'paketSoal'
    kodePaket = Column(String(30), primary_key=True, nullable=False)
    tanggal = Column(String(255))
    deskripsi = Column(String(255))


def main():
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()
