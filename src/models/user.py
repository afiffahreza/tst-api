from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import Column, Integer, String
from db import Base
from db import ENGINE

class UserTable(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    email = Column(String(30), nullable=False)
    name = Column(String(30), nullable=False)
    disabled = Column(Boolean)
    

def main():
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()