from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, engine


###Cracion de tablas base de datos
class UserTable(Base):
    __tablename__="Tareas"
    id: Mapped[int]= mapped_column(Integer, primary_key=True)
    nombre: Mapped[str]= mapped_column(String(30))
    fecha: Mapped[int]= mapped_column (Integer())
    descripcion: Mapped[str]= mapped_column(String[30])
    owner_id: Mapped[int]= mapped_column(ForeignKey("Usuarios.id"))
    owner: Mapped["UsuariosTable"]= relationship(back_populates="tareas")

class UsuariosTable(Base):
    __tablename__="Usuarios"
    id: Mapped[int]= mapped_column(Integer, primary_key=True)
    username: Mapped[str]= mapped_column(String(15),unique=True)
    email: Mapped[str]= mapped_column(String(50),unique=True,index=True)
    password_hash: Mapped[str]= mapped_column (String(200))
    tareas: Mapped[list["UserTable"]]= relationship(back_populates="owner")

Base.metadata.create_all(bind=engine)