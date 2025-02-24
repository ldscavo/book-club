from sqlmodel import Field, SQLModel, AutoString, Relationship
from pydantic import EmailStr
from datetime import datetime, timedelta
import secrets


class ClubMember(SQLModel, table=True):
    club_id: int | None = Field(default=None,
                                foreign_key="club.id",
                                primary_key=True)

    member_id: int | None = Field(default=None,
                                  foreign_key="user.id",
                                  primary_key=True)


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, sa_type=AutoString)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    password: bytes

    clubs_owned: list["Club"] = Relationship(back_populates="owner")
    clubs_joined: list["Club"] = Relationship(back_populates="members",
                                              link_model=ClubMember)

    created_at: datetime = Field(default=datetime.now(), exclude=True)
    update_at: datetime = Field(default=datetime.now(), exclude=True)


class UserPublic(UserBase):
    id: int


class Token(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    token: str = Field(unique=True, default=secrets.token_hex(16))
    expires_at: datetime = Field(default=datetime.now() + timedelta(days=7))

    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship()


class ClubBase(SQLModel):
    name: str = Field(nullable=False)
    description: str | None = Field(default=None, nullable=True)


class Club(ClubBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    owner_id: int = Field(foreign_key="user.id")
    owner: User = Relationship(back_populates="clubs_owned")

    members: list["User"] = Relationship(back_populates="clubs_joined",
                                         link_model=ClubMember)

    invitations: list["Invitation"] = Relationship()

    created_at: datetime = Field(default=datetime.now(), exclude=True)
    update_at: datetime = Field(default=datetime.now(), exclude=True)


class ClubPublic(ClubBase):
    id: int
    members: list["UserPublic"]
    invitations: list["Invitation"]


class InvitationBase(SQLModel):
    club_id: int | None = Field(default=None,
                                foreign_key="club.id",
                                primary_key=True)

    email: EmailStr = Field(primary_key=True,
                            sa_type=AutoString)


class Invitation(InvitationBase, table=True):
    invited_at: datetime = Field(default=datetime.now(), exclude=True)
