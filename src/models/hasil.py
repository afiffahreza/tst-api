from sqlalchemy import Column, Integer, String
from db import Base
from db import ENGINE


class HasilTable(Base):
    __tablename__ = 'hasil'
    username = Column(String(30), primary_key=True, nullable=False)
    kodePaket = Column(String(16), primary_key=True, nullable=False)
    nilai = Column(Integer)
    ranking = Column(Integer)


def main():
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()
