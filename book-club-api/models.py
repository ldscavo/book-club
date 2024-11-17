from sqlmodel import Field, SQLModel
from datetime import datetime


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str
    password: str
    created_at: datetime = Field(default=datetime.now())
    update_at: datetime = Field(default=datetime.now())
