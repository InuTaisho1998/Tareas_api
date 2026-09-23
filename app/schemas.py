from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field

##Modelos pydantic

class TaskCreate(BaseModel):
    name: str = Field(
        description="full name of the task",
        min_length=2,
        max_length=50
    )
    deadline: date = Field(
        description="date limite de la tarea")
    description: str = Field(
        description="Assignment deadline",
        min_length=2,
        max_length=50
    )
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "name": "FakeTask",
                "date": "2026-02-10",
                "task_description": "Fakedescription"
            }]
        }
    }


class UsersCreate(BaseModel):
    username: str = Field(
        description="User's full name",
        min_length=2,
        max_length=50
    )
    email: EmailStr = Field(
        description="User email",
        min_length=5,
        max_length=50
    )
    password: str = Field(
        description="Secure password",
        min_length=7,
        max_length=50
    )
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "username": "Fakename",
                "email": "Fakeemail@gmail.com",
                "password": "Fakepassword123"
            }]
        }
    }

class TokenResponse(BaseModel):
    access_token: str = Field(
        description="access token in str"
    )
    token_type: str = Field(
        description="access token in str"
    )

class TaskResponse(BaseModel):
    id: int = Field(
        description="id identificador de la tarea"
    )
    name: str = Field(
        description="name de la tarea"
    )
    deadline: date = Field(
        description="date limite de la tarea"
    )
    description: str = Field(
        description="description de la tarea"
    )

    model_config = ConfigDict(from_attributes=True)


class TasksResponse(BaseModel):
    tasks: list[TaskResponse] = Field(
        description="modelo de respuesta para consulta de varias tareas al tiempo"
    )

    model_config = ConfigDict(from_attributes=True)