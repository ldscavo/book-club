from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select
from fastapi import HTTPException
from database import db_engine
import bcrypt
from models import User


class RegistrationModel(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str


def register_user(reg: RegistrationModel) -> User:
    with Session(db_engine) as session:
        if reg.password != reg.password_confirm:
            raise HTTPException(
                status_code=422,
                detail="Passwords don't match!"
            )

        existing_user = session.exec(
            select(User).where(User.email == reg.email)
        ).one_or_none()

        if existing_user is not None:
            raise HTTPException(
                status_code=422,
                detail="User with that email already exists!"
            )

        password_hash = bcrypt.hashpw(
            bytes(bytearray(reg.password, 'utf-8')),
            bcrypt.gensalt()
        )

        user = User(email=reg.email, password=password_hash)
        session.add(user)
        session.commit()

        session.refresh(user)
        return user
