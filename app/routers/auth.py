from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import UsuariosTable
from app.security import create_access_token, generate_password_hash, verify_password
from app.shemas import TokenResponse, Usuarios

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/registrase/API/V1", status_code=201, response_model=TokenResponse)
def registrar(data: Usuarios, db: Session = Depends(get_db)): #noqa: B008
    username = db.query(UsuariosTable).filter(UsuariosTable.username == data.username).first()
    email = db.query(UsuariosTable).filter(UsuariosTable.email == data.email).first()
    if email or username:
        raise HTTPException(status_code=409, detail="Datos ya existentes")
    
    hasheada = generate_password_hash(password=data.password)
    nuevo = UsuariosTable(username=data.username, email=data.email, password_hash=hasheada)

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    token = create_access_token({"sub": data.username})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login/API/V1", status_code=200, response_model=TokenResponse)
def login(Form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)): #noqa: B008
    user = db.query(UsuariosTable).filter(UsuariosTable.username == Form.username).first()
    if not user or not verify_password(password_plana=Form.password, hash_guardado=user.password_hash):
        raise HTTPException(status_code=401, detail="Datos Incorrectos")
    
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}