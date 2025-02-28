from fastapi import APIRouter, Depends
from database import Session, get_session
from pydantic import EmailStr
from models import Club, ClubPublic, UserPublic
from auth.handler import get_current_user
from clubs.handler import (
    get_users_clubs,
    get_club,
    create_club,
    UserClubs,
    NewClubModel,
    update_club
)

router = APIRouter(prefix="/clubs")


@router.get("/")
def clubs(user: UserPublic = Depends(get_current_user),
          session: Session = Depends(get_session)) -> UserClubs:
    return get_users_clubs(user.id, session)


@router.post("/")
def new_club(*, user: UserPublic = Depends(get_current_user),
             session: Session = Depends(get_session),
             new_club: NewClubModel) -> Club:
    return create_club(user.id, new_club, session)


@router.get("/{id}")
def club(*, session: Session = Depends(get_session),
         id: int) -> Club:
    return get_club(id, session)


@router.put("/{id}")
def modify_club(*, session: Session = Depends(get_session),
                id: int,
                update: NewClubModel) -> Club:
    club = ClubPublic(id=id,
                      name=update.name,
                      description=update.description,
                      members=[],
                      invitations=[])
    return update_club(club, session)
