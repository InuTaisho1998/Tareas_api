import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.config import Settings
from app.database import get_db
from app.models import TasksTable, UserTable
from app.schemas import TaskCreate, TaskResponse, TasksResponse

router = APIRouter(prefix="/api/v1", tags=["tasks"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/register")

# Helper function to get current user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)): #noqa: B008
    try:
        payload = jwt.decode(token, Settings.SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Unauthorized")    
    
    user = db.query(UserTable).filter(UserTable.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user

@router.post("/tasks", status_code=201, response_model=TaskResponse) 
def create_task(data: TaskCreate, db: Session = Depends(get_db), user = Depends(get_current_user)): #noqa: B008
    newtask = TasksTable(
        name=data.name,
        deadline=data.deadline,
        description=data.description,
        owner_id=user.id 
    )

    db.add(newtask)
    db.commit()
    db.refresh(newtask)

    return {"id": newtask.id, "name": newtask.name, "deadline": newtask.deadline, "description": newtask.description}

@router.get("/tasks/{tasks_id}", status_code=200, response_model=TaskResponse)
def consult_user_task_by_ID(tasks_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)): #noqa: B008
    task = db.query(TasksTable).filter(TasksTable.id == tasks_id, TasksTable.owner_id == user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"id": task.id, "name": task.name, "deadline": task.deadline, "description": task.description}

@router.get("/tasks", status_code=200, response_model=TasksResponse)
def get_task(db: Session = Depends(get_db), user = Depends(get_current_user)): #noqa: B008
    user_Tasks = db.query(TasksTable).filter(TasksTable.owner_id == user.id).all()

    return {"tasks": user_Tasks}

@router.put("/tasks/{tasks_id}", status_code=200, response_model=TaskResponse)
def update_task(tasks_id: int, data: TaskCreate, db: Session = Depends(get_db), user = Depends(get_current_user)): #noqa: B008
    task_to_update = db.query(TasksTable).filter(TasksTable.id == tasks_id, TasksTable.owner_id == user.id).first()
    if not task_to_update:
        raise HTTPException(status_code=404, detail="Task not found")
        
    task_to_update.name = data.name
    task_to_update.deadline = data.deadline
    task_to_update.description = data.description

    db.commit()
    db.refresh(task_to_update)

    return {"id": task_to_update.id, "name": task_to_update.name, "deadline": task_to_update.deadline, "description": task_to_update.description}

@router.delete("/tasks/{tasks_id}", status_code=204)
def eliminar_task(tasks_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)): #noqa: B008
    delete = db.query(TasksTable).filter(TasksTable.id == tasks_id, TasksTable.owner_id == user.id).first()
    if not delete:
        raise HTTPException(status_code=404, detail="Task not found")
        
    db.delete(delete)
    db.commit()