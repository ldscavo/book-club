from sqlmodel import Field, SQLModel, AutoString, Relationship
from pydantic import EmailStr
from datetime import datetime


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    email: EmailStr = Field(unique=True, sa_type=AutoString)
    password: bytes

    created_at: datetime = Field(default=datetime.now())
    update_at: datetime = Field(default=datetime.now())


class Token(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    token: str = Field(unique=True)

    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship()
