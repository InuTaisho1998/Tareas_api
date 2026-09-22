import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

URL_DB=os.getenv("URL_DB")

######Conetion Data Base
engine= create_engine(url=URL_DB)
SessionLocal=sessionmaker(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base=declarative_base()