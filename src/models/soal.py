from sqlalchemy import Column, Integer, String
from db import Base
from db import ENGINE


# Bikin class model


def main():
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()
