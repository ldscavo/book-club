from pydantic import BaseModel, EmailStr
from typing import Annotated
from sqlmodel import Session, select
from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader
import bcrypt
from models import User, Token
from database import db_engine
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
        query = select(Token).where(Token.token == token)
        user_token = session.exec(query).one_or_none()

        if user_token is None:
            raise unauthorize_exception

        if user_token.expires_at < datetime.now():
            # Token has expired, remove from database
            session.delete(user_token)
            session.commit()
            raise unauthorize_exception

        return user_token.user


def register_user(reg: RegistrationModel, session: Session) -> User:
    if reg.password != reg.password_confirm:
        raise HTTPException(status_code=422,
                            detail="Passwords don't match!")

    query = select(User).where(User.email == reg.email)
    existing_user = session.exec(query).one_or_none()

    if existing_user is not None:
        raise HTTPException(status_code=422,
                            detail="User with that email already exists!")

    password_hash = bcrypt.hashpw(to_bytes(reg.password), bcrypt.gensalt())

    user = User(email=reg.email, password=password_hash)
    session.add(user)
    session.commit()
    session.refresh(user)

    if user.id is None:
        raise HTTPException(status_code=422,
                            detail="User with that email already exists!")

    token = Token(user_id=user.id)
    session.add(token)
    session.commit()
    session.refresh(token)

    return user


def login_user(login: LoginModel, session: Session) -> Token:
    query = select(User).where(User.email == login.email)
    user = session.exec(query).one_or_none()

    if user is None or user.id is None:
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


def to_bytes(password: str) -> bytes:
    return bytes(bytearray(password, 'utf-8'))
