from sqlmodel import Field, SQLModel, AutoString
from pydantic import EmailStr, SecretStr
from datetime import datetime


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True, sa_type=AutoString)
    password: SecretStr = Field(sa_type=AutoString)
    created_at: datetime = Field(default=datetime.now())
    update_at: datetime = Field(default=datetime.now())
