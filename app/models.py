from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base, engine


###Cracion de tablas base de datos
class TasksTable(Base):
    __tablename__="Tasks"
    id: Mapped[int]= mapped_column(Integer, primary_key=True)
    name: Mapped[str]= mapped_column(String(30))
    deadline: Mapped[date]= mapped_column (Date())
    description: Mapped[str]= mapped_column(String(30))
    owner_id: Mapped[int]= mapped_column(ForeignKey("Users.id"))
    owner: Mapped["UserTable"]= relationship(back_populates="tasks")

class UserTable(Base):
    __tablename__="Users"
    id: Mapped[int]= mapped_column(Integer, primary_key=True)
    username: Mapped[str]= mapped_column(String(15),unique=True)
    email: Mapped[str]= mapped_column(String(50),unique=True,index=True)
    password_hash: Mapped[str]= mapped_column (String(200))
    tasks: Mapped[list["TasksTable"]]= relationship(back_populates="owner")

Base.metadata.create_all(bind=engine)