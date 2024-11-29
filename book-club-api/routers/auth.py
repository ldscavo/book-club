from fastapi import APIRouter, Depends
from sqlmodel import Session
from models import User, Token
from database import get_session
from handlers.auth import (
    register_user, login_user, RegistrationModel, LoginModel
)


router = APIRouter()


@router.post("/register")
async def register(reg: RegistrationModel,
                   session: Session = Depends(get_session)) -> User:
    return register_user(reg, session)


@router.post("/login")
def login(login: LoginModel,
          session: Session = Depends(get_session)) -> Token:
    return login_user(login, session)
