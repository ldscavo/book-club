from fastapi import APIRouter, Response, status
from pydantic import BaseModel
from models import User

router = APIRouter(
    prefix="/users"
)


class RegistrationModel(BaseModel):
    email: str
    password: str
    password_confirm: str


@router.post("/register")
async def register(reg: RegistrationModel, resp: Response):
    if reg.password != reg.password_confirm:
        resp.status_code = status.HTTP_400_BAD_REQUEST
        return "NO"

    # user = User(email=reg.email)

    return {"foo": "bar"}
