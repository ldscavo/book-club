from fastapi import APIRouter, Depends
from database import Session, get_session
from models import User, Club
from handlers.auth import get_current_user
from handlers.clubs import get_users_clubs, create_club, UserClubs

router = APIRouter(prefix="/clubs")


@router.get("/")
def clubs(user: User = Depends(get_current_user),
          session: Session = Depends(get_session)) -> UserClubs:
    return get_users_clubs(user.id, session)


@router.post("/")
def new_club(*, user: User = Depends(get_current_user),
             session: Session = Depends(get_session),
             new_club: Club) -> Club:
    return create_club(user.id, new_club, session)
