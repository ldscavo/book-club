from fastapi import APIRouter, Depends
from sqlalchemy.orm import session
from auth.handler import get_current_user
from database import Session, get_session
from pydantic import EmailStr
from models import Club, Invitation, User
from invitations.handler import (
    get_invitations_by_club,
    get_invitations_by_email,
    invite_to_club,
    remove_invitation
)


club_router = APIRouter(prefix="/clubs/{club_id}/invitations")


@club_router.get("/")
def club_invitations(*, session: Session = Depends(get_session),
           club_id: int) -> list[Invitation]:
    return get_invitations_by_club(club_id, session)


@club_router.post("/")
def invite(*, session: Session = Depends(get_session),
           club_id: int,
           emails: list[EmailStr]) -> Club:
    return invite_to_club(club_id, emails, session)


@club_router.delete("/{id}")
def rescind_invitation(*, session: Session = Depends(get_session),
                       club_id: int,
                       email: EmailStr) -> None:
    return remove_invitation(club_id, email, session)


user_router = APIRouter(prefix="/users/me/invitations")

@user_router.get("/")
def my_invitations(*, user: User = Depends(get_current_user),
                   session: Session = Depends(get_session)) -> list[Invitation]:
    return get_invitations_by_email(user.email, session)
