from pydantic import BaseModel, EmailStr
from typing import Annotated
from sqlmodel import Session, select
from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader
from database import db_engine
import bcrypt
from models import User, Token
from datetime import datetime


class RegistrationModel(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str


class LoginModel(BaseModel):
    email: EmailStr
    password: str


header_scheme = APIKeyHeader(name="x-key")

unauthorize_exception = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(token: Annotated[str, Depends(header_scheme)]):
    with Session(db_engine) as session:
        token = session.exec(
            select(Token).where(Token.token == token)
        ).one_or_none()

        if token is None:
            raise unauthorize_exception

        if token.expires_at < datetime.now():
            raise unauthorize_exception

        return token.user


def register_user(reg: RegistrationModel) -> User:
    with Session(db_engine) as session:
        if reg.password != reg.password_confirm:
            raise HTTPException(status_code=422,
                                detail="Passwords don't match!")

        existing_user = session.exec(
            select(User).where(User.email == reg.email)
        ).one_or_none()

        if existing_user is not None:
            raise HTTPException(status_code=422,
                                detail="User with that email already exists!")

        password_hash = bcrypt.hashpw(to_bytes(reg.password), bcrypt.gensalt())

        user = User(email=reg.email, password=password_hash)
        session.add(user)
        session.commit()
        session.refresh(user)

        token = Token(user_id=user.id)
        session.add(token)
        session.commit()
        session.refresh(token)

        return token


def login_user(login: LoginModel) -> Token:
    with Session(db_engine) as session:
        user = session.exec(select(User).where(
            User.email == login.email)).one_or_none()

        if user is None:
            raise HTTPException(status_code=422, detail="Invalid email")
        print(login.password)
        is_valid_pw = bcrypt.checkpw(to_bytes(login.password), user.password)

        if not is_valid_pw:
            raise HTTPException(status_code=422, detail="Invalid password")

        token = Token(user_id=user.id)
        session.add(token)
        session.commit()

        session.refresh(token)
        return token


def validate_user_token(token: str) -> bool:
    with Session(db_engine) as session:
        token = session.exec(
            select(Token).where(Token.token == token)
        ).one_or_none()

        if token is None:
            return False

        return True


def to_bytes(password: str) -> bytes:
    return bytes(bytearray(password, 'utf-8'))
