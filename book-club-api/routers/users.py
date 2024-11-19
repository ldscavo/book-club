from fastapi import APIRouter, Response, status
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select
import bcrypt
from database import db_engine
from models import User

router = APIRouter(
    prefix="/users"
)


class RegistrationModel(BaseModel):
    email: EmailStr
    password: str
    password_confirm: str


class Error(BaseModel):
    msg: str


@router.post("/register")
async def register(reg: RegistrationModel, resp: Response) -> User | Error:
    with Session(db_engine) as session:
        if reg.password != reg.password_confirm:
            resp.status_code = status.HTTP_400_BAD_REQUEST
            return Error(msg="Passwords don't match!")

        existing_user = session.exec(
            select(User).where(User.email == reg.email)
        ).one_or_none()

        if existing_user is not None:
            print(existing_user)
            resp.status_code = status.HTTP_400_BAD_REQUEST
            return Error(msg="User with that email already exists!")

        password_hash = bcrypt.hashpw(
            bytes(bytearray(reg.password, 'utf-8')), bcrypt.gensalt())

        user = User(email=reg.email, password=password_hash)
        session.add(user)
        session.commit()

        session.refresh(user)
        return user
