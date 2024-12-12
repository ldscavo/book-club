from pydantic import BaseModel
from database import Session
from models import User, Club, ClubPublic


class UserClubs(BaseModel):
    owned: list[ClubPublic]
    joined: list[ClubPublic]


class NewClubModel(BaseModel):
    name: str
    description: str | None


def get_users_clubs(user_id: int, session: Session) -> UserClubs:
    user = session.get(User, user_id)
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
