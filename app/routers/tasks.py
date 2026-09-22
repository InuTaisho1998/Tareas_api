import os

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import UserTable, UsuariosTable
from app.shemas import TareaResponse, Tareas, TareasResponse

SECRET_KEY = os.getenv("SECRET_KEY")

router = APIRouter(prefix="/tareas", tags=["Tareas"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/API/V1")

# Helper function to get current user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)): #noqa: B008
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="No autorizado")    
    
    user = db.query(UsuariosTable).filter(UsuariosTable.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="No autorizado")
    return user

@router.post("/crear_tarea/API/V1", status_code=201, response_model=TareaResponse) 
def crear_tarea(data: Tareas, db: Session = Depends(get_db), usuario = Depends(get_current_user)): #noqa: B008
    newtarea = UserTable(
        nombre=data.nombre,
        fecha=data.fecha,
        descripcion=data.descripcion,
        owner_id=usuario.id 
    )

    db.add(newtarea)
    db.commit()
    db.refresh(newtarea)
    return {"id": newtarea.id, "nombre": newtarea.nombre, "fecha": newtarea.fecha, "descripcion": newtarea.descripcion}

@router.get("/consultar_tarea_usuario_por_ID/API/V1/{tarea_id}", status_code=200, response_model=TareaResponse)
def consultar_tarea_por_ID(tarea_id: int, db: Session = Depends(get_db), usuario = Depends(get_current_user)): #noqa: B008
    tarea = db.query(UserTable).filter(UserTable.id == tarea_id, UserTable.owner_id == usuario.id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"id": tarea.id, "nombre": tarea.nombre, "fecha": tarea.fecha, "descripcion": tarea.descripcion}

@router.get("/consultar_tareas_usuario/API/V1", status_code=200, response_model=TareasResponse)
def tareas(db: Session = Depends(get_db), usuario = Depends(get_current_user)): #noqa: B008
    user_tareas = db.query(UserTable).filter(UserTable.owner_id == usuario.id).all()
    return {"tareas": user_tareas}

@router.put("/actualizar_tarea/API/V1/{tarea_id}", status_code=200, response_model=TareaResponse)
def actualizar_tarea(tarea_id: int, data: Tareas, db: Session = Depends(get_db), usuario = Depends(get_current_user)): #noqa: B008
    tarea_a_actualizar = db.query(UserTable).filter(UserTable.id == tarea_id, UserTable.owner_id == usuario.id).first()
    if not tarea_a_actualizar:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
    tarea_a_actualizar.nombre = data.nombre
    tarea_a_actualizar.fecha = data.fecha
    tarea_a_actualizar.descripcion = data.descripcion

    db.commit()
    db.refresh(tarea_a_actualizar)
    return {"id": tarea_a_actualizar.id, "nombre": tarea_a_actualizar.nombre, "fecha": tarea_a_actualizar.fecha, "descripcion": tarea_a_actualizar.descripcion}

@router.delete("/eliminar_tarea/API/V1/{tarea_id}", status_code=204)
def eliminar_tarea(tarea_id: int, db: Session = Depends(get_db), usuario = Depends(get_current_user)): #noqa: B008
    delete = db.query(UserTable).filter(UserTable.id == tarea_id, UserTable.owner_id == usuario.id).first()
    if not delete:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
    db.delete(delete)
    db.commit()