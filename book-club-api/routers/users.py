from fastapi import APIRouter, Depends
from models import User, UserPublic
from handlers.auth import get_current_user


router = APIRouter(prefix="/users")


@router.get("/me", response_model=UserPublic)
def me(user: User = Depends(get_current_user)) -> User:
    return user
