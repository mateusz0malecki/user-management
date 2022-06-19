from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

postgres_user = os.environ["POSTGRES_USER"]
postgres_db = os.environ["POSTGRES_DB"]
postgres_password = os.environ["POSTGRES_PASSWORD"]
postgres_host = os.environ["POSTGRES_HOST"]

SQLALCHEMY_DATABASE_URL = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_db}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
