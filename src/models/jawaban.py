from sqlalchemy import Column, Integer, String
from db import Base
from db import ENGINE


# Bikin class model
class jawaban(Base):
    __tablename__ = 'jawaban'
    username = Column(String(30), primary_key=True, nullable=False)
    kodePaket = Column(String(16), primary_key=True, nullable=False)
    kodeSoal = Column(Integer, primary_key=True, nullable=False)
    jawaban = Column(Integer)

def main():
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()
