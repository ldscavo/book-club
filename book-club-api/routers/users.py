from fastapi import APIRouter, Response, status
from pydantic import BaseModel, EmailStr, SecretStr
from sqlmodel import Session, select
from database import db_engine
from models import User

router = APIRouter(
    prefix="/users"
)


class RegistrationModel(BaseModel):
    email: EmailStr
    password: SecretStr
    password_confirm: SecretStr


@router.post("/register")
async def register(reg: RegistrationModel, resp: Response):
    with Session(db_engine) as session:
        if reg.password != reg.password_confirm:
            resp.status_code = status.HTTP_400_BAD_REQUEST
            return "NO"

        existing_user = session.exec(
            select(User).where(User.email == reg.email)
        ).one_or_none

        if existing_user is not None:
            resp.status_code = status.HTTP_400_BAD_REQUEST
            return "NO"

        user = User(email=reg.email)
        session.add(user)
        session.commit()

        session.refresh(user)
        return user
