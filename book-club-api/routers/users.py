from fastapi import APIRouter, Response
from models import User, Token
from handlers.users import register_user, RegistrationModel, login_user, LoginModel


router = APIRouter(prefix="/users")


@router.post("/register")
async def register(reg: RegistrationModel, resp: Response) -> User:
    return register_user(reg)


@router.post("/login")
def login(login: LoginModel, resp: Response) -> Token:
    return login_user(login)
