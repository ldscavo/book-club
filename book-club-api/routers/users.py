from fastapi import APIRouter
from ..models import User

router = APIRouter(
    prefix="/users"
)


@router.post("/register")
async def register(user: User):
    return {"foo": "bar"}
