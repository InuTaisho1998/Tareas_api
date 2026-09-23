from config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


URL_DB = settings.DATABASE_URL

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