from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select
from fastapi import HTTPException
from database import db_engine
import bcrypt
import jwt
from models import User, Token
import settings


class RegistrationModel(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str


class LoginModel(BaseModel):
    email: EmailStr
    password: str


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


def login_user(login: LoginModel) -> Token:
    with Session(db_engine) as session:
        user = session.exec(
            select(User).where(User.email == login.email)
        ).one_or_none()

        if user is None:
            raise HTTPException(
                status_code=422,
                detail="Invalid email"
            )

        is_valid_pw = bcrypt.checkpw(
            bytes(bytearray(login.password, 'utf-8')),
            user.password
        )

        if not is_valid_pw:
            raise HTTPException(
                status_code=422,
                detail="Invalid password"
            )

        jwt_value = jwt.encode(
            {"user_id": user.id},
            settings.SECRET,
            algorithm="HS256"
        )

        token = Token(user_id=user.id, token=jwt_value)
        session.add(token)
        session.commit()

        session.refresh(token)
        return token
