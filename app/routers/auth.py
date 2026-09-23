from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import UserTable
from app.schemas import TokenResponse, UsersCreate
from app.security import create_access_token, generate_password_hash, verify_password

router = APIRouter(prefix="/api/v1", tags=["auth"])

@router.post("/auth/register", status_code=201, response_model=TokenResponse)
def registrar(data: UsersCreate, db: Session = Depends(get_db)): #noqa: B008
    username = db.query(UserTable).filter(UserTable.username == data.username).first()
    email = db.query(UserTable).filter(UserTable.email == data.email).first()
    if email or username:
        raise HTTPException(status_code=409, detail="Existing data")
    
    hasheada = generate_password_hash(password=data.password)
    nuevo = UserTable(username=data.username, email=data.email, password_hash=hasheada)

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    token = create_access_token({"sub": data.username})

    return {"access_token": token, "token_type": "bearer"}


@router.post("/auth/login", status_code=200, response_model=TokenResponse)
def login(Form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)): #noqa: B008
    user = db.query(UserTable).filter(UserTable.username == Form.username).first()
    if not user or not verify_password(password_plana=Form.password, hash_guardado=user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect data")
    
    token = create_access_token({"sub": user.username})
    
    return {"access_token": token, "token_type": "bearer"}