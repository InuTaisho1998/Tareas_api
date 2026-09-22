import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ["URL_DB"] = "sqlite:///./test.db"
os.environ["SECRET_KEY"] = "askfgjdgasdfgkgasdkhfhjfgsdakhgasdhfjhasdgfjsdafvgasdfhjhsafsjdsdavfokmasvbfkasdvfafiopj"

from app.database import Base, get_db
from app.main import app

DB_URL = "sqlite:///./test.db"
engine = create_engine(url=DB_URL, connect_args={"check_same_thread": False})
SessionTesting = sessionmaker(autoflush=False, autocommit=False, bind=engine)

@pytest.fixture(autouse=True)
def create_table():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def cliente():
    def get_db_test():
        db = SessionTesting()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = get_db_test 
    yield TestClient(app)
    app.dependency_overrides.clear()