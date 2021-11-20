from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import DateTime
from db import Base
from db import ENGINE


class PaketTable(Base):
    __tablename__ = 'paketSoal'
    kodePaket = Column(String(16), primary_key=True, nullable=False)
    tanggal = Column(DateTime)
    deskripsi = Column(String(256))


def main():
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()
