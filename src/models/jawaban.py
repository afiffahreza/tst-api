from sqlalchemy import Column, Integer, String
from db import Base
from db import ENGINE


# Bikin class model
class JawabanTable(Base):
    __tablename__ = 'jawaban'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30), nullable=False)
    kodePaket = Column(String(30), nullable=False)
    kodeSoal = Column(Integer, nullable=False)
    jawaban = Column(String(30))

def main():
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()
