from sqlalchemy import Column, Integer, String
from db import Base
from db import ENGINE


# Bikin class model
class PembelianTable(Base):
    __tablename__ = 'pembelian'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30), nullable=False)
    kodePaket = Column(String(30), nullable=False)

def main():
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()
