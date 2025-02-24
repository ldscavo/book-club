from fastapi import HTTPException
from pydantic import BaseModel, EmailStr
from database import Session
from models import User, Club, ClubPublic, Invitation


class UserClubs(BaseModel):
    owned: list[Club]
    joined: list[Club]


class NewClubModel(BaseModel):
    name: str
    description: str | None


def get_users_clubs(user_id: int, session: Session) -> UserClubs:
    user = session.get(User, user_id)
    
    if user is None:
        raise HTTPException(404, "Could not find user")

    return UserClubs(owned=user.clubs_owned, joined=user.clubs_joined)


def create_club(user_id: int,
                new_club: NewClubModel,
                session: Session) -> Club:

    club = Club(owner_id=user_id,
                name=new_club.name,
                description=new_club.description)
    session.add(club)
    session.commit()
    session.refresh(club)

    return club


def get_club(club_id: int, session: Session) -> Club:
    club = session.get(Club, club_id)

    if club is None:
        raise HTTPException(404, "Could not find club")

    return club


def update_club(updated_club: ClubPublic,
                session: Session) -> Club:
    club = get_club(updated_club.id, session)
    if club is None:
        raise HTTPException(404, "Could not find club")

    club.name = updated_club.name
    club.description = updated_club.description


    session.add(club)
    session.commit()
    session.refresh(club)
    return club

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
