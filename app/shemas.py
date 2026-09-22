from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field

##Modelos pydantic

class Tareas(BaseModel):
    nombre: str = Field(
        description="Nombre completo de la tarea",
        min_length=2,
        max_length=50
    )
    fecha: date = Field(
        description="Fecha limite de la tarea")
    descripcion: str = Field(
        description="description completa de la tarea",
        min_length=2,
        max_length=50
    )
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "nombre": "FakeTask",
                "fecha": "2026-02-10",
                "description": "Fakedescription"
            }]
        }
    }


class Usuarios(BaseModel):
    username: str = Field(
        description="Nombre completo del usuario",
        min_length=2,
        max_length=50
    )
    email: EmailStr = Field(
        description="Correo del usuario",
        min_length=5,
        max_length=50
    )
    password: str = Field(
        description="Contrasena segura",
        min_length=7,
        max_length=50
    )
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "username": "FakeNombre",
                "email": "Fakeemail@gmail.com",
                "password": "Fakepassword123"
            }]
        }
    }

class TokenResponse(BaseModel):
    access_token: str = Field(
        description="token de acceso en str"
    )
    token_type: str = Field(
        description="tipo de token de acceso"
    )

class TareaResponse(BaseModel):
    id: int = Field(
        description="id identificador de la tarea"
    )
    nombre: str = Field(
        description="nombre de la tarea"
    )
    fecha: date = Field(
        description="fecha limite de la tarea"
    )
    descripcion: str = Field(
        description="description de la tarea"
    )

    model_config = ConfigDict(From_attributes=True)


class TareasResponse(BaseModel):
    tareas: list[TareaResponse] = Field(
        description="modelo de respuesta para consulta de varias tareas al tiempo"
    )

    model_config = ConfigDict(From_attributes=True)