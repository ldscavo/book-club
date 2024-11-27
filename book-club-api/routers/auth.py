from fastapi import APIRouter, Response
from models import User, Token
from handlers.auth import (
    register_user, login_user, RegistrationModel, LoginModel
)


router = APIRouter()


@router.post("/register")
async def register(reg: RegistrationModel, resp: Response) -> User:
    return register_user(reg)


@router.post("/login")
def login(login: LoginModel) -> Token:
    return login_user(login)
