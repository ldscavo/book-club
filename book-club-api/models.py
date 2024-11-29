from sqlmodel import Field, SQLModel, AutoString, Relationship
from pydantic import EmailStr
from datetime import datetime, timedelta
import secrets


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    email: EmailStr = Field(unique=True, sa_type=AutoString)
    password: bytes

    clubs_owned: list["Club"] = Relationship(back_populates="owner")
    clubs_joined: list["Club"] = Relationship(back_populates="members")

    created_at: datetime = Field(default=datetime.now())
    update_at: datetime = Field(default=datetime.now())


class Token(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    token: str = Field(unique=True, default=secrets.token_hex(16))
    expires_at: datetime = Field(default=datetime.now() + timedelta(days=7))

    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship()


class Club(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    owner_id: int = Field(foreign_key="user.id")
    owner: User = Relationship(back_populates="clubs_owned")

    name: str = Field(nullable=False)
    description: str = Field(nullable=True)

    members: list["User"] = Relationship(back_populates="clubs_joined")

    created_at: datetime = Field(default=datetime.now())
    update_at: datetime = Field(default=datetime.now())


class ClubMember(SQLModel, table=True):
    club_id: int | None = Field(default=None,
                                foreign_key="club.id",
                                primary_key=True)

    member_id: int | None = Field(default=None,
                                  foreign_key="user.id",
                                  primary_key=True)
