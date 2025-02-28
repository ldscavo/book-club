from fastapi import HTTPException
from pydantic import EmailStr
from sqlmodel import select
from clubs.handler import get_club
from database import Session
from models import Club, Invitation

def get_invitations(club_id: int,
                    session: Session) -> list[Invitation]:
    club = get_club(club_id, session)

    return club.invitations

def invite_to_club(club_id: int,
                   emails: list[EmailStr],
                   session: Session) -> Club:
    club = get_club(club_id, session)

    if club is None:
        raise HTTPException(404, "Could not find club")

    for email in emails:
        club.invitations.append(Invitation(email=email))

    session.commit()
    session.refresh(club)

    return club

def remove_invitation(club_id: int,
                      email: EmailStr,
                      session: Session) -> None:
    query = select(Invitation).where(Invitation.club_id == club_id).where(Invitation.email == email)
    invite = session.exec(query).one_or_none()

    if invite is None:
        raise HTTPException(404, "Could not find invitation")

    session.delete(invite)
    session.commit()
