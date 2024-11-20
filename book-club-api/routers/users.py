from fastapi import APIRouter, Response
from models import User
from handlers.users import register_user, RegistrationModel


router = APIRouter(prefix="/users")


@router.post("/register")
async def register(reg: RegistrationModel, resp: Response) -> User:
    return register_user(reg)
