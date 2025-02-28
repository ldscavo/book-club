from fastapi import APIRouter, Depends
from database import Session, get_session
from pydantic import EmailStr
from models import Club, Invitation
from invitations.handler import (
    get_invitations,
    invite_to_club,
    remove_invitation
)

router = APIRouter(prefix="/clubs/{club_id}/invitations")

@router.get("/")
def club_invitations(*, session: Session = Depends(get_session),
           club_id: int) -> list[Invitation]:
    return get_invitations(club_id, session)

@router.post("/")
def invite(*, session: Session = Depends(get_session),
           club_id: int,
           emails: list[EmailStr]) -> Club:
    return invite_to_club(club_id, emails, session)

@router.delete("/{id}")
def rescind_invitation(*, session: Session = Depends(get_session),
                       club_id: int,
                       email: EmailStr) -> None:
    return remove_invitation(club_id, email, session)
