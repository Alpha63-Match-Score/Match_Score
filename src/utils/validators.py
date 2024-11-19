from datetime import datetime, timezone, timedelta
from typing import Type
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from src.models import Tournament, Match, User, Player
from src.models.enums import Stage, Role, TournamentFormat
from src.models.team import Team
from src.schemas.schemas import UserResponse


# existing validators
def tournament_exists(db: Session, tournament_id: UUID) -> Type[Tournament]:
    tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if not tournament:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Tournament not found")

    return tournament


def team_exists(
        db: Session,
        team_id: UUID | None = None,
        team_name: str | None = None
) -> Type[Team]:

    team = None
    if team_id:
        team = db.query(Team).filter(Team.id == team_id).first()
    elif team_name:
        team = db.query(Team).filter(Team.name == team_name).first()

    if not team:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Team not found")

    return team


def match_exists(db: Session, match_id: UUID) -> Type[Match]:
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Match not found")

    return match


def user_exists(db: Session, user_id: UUID) -> Type[User]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    return user


def player_exists(db: Session, username: str) -> Type[Player]:
    player = db.query(Player).filter(Player.username == username).first()
    if not player:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Player not found")

    return player


def user_email_exists(db: Session, email: str) -> None:
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Email already exists")


def tournament_title_unique(db: Session, title: str) -> None:
    if db.query(Tournament).filter(Tournament.title == title).first():
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Tournament with this title already exists")


# authorisation validators
def director_or_admin(user: UserResponse) -> None:
    if user.role not in [Role.DIRECTOR, Role.ADMIN]:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="You are not authorized to perform this action")


def is_author_of_tournament(db: Session, tournament_id: UUID, user_id: UUID) -> None:
    db_tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if db_tournament.director_id != user_id:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="You are not authorized to perform this action")


# role validators
def user_role_is_director(current_user: User) -> None:
    if current_user.role == Role.DIRECTOR:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="User is already a director.")


def user_role_is_admin(current_user: User) -> None:
    if current_user.role != Role.ADMIN:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Only admins can perform this action.")


def user_role_is_player(current_user: User) -> None:
    if current_user.role == Role.PLAYER:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="User is already a player.")


# datetime validators
def validate_start_date(start_date) -> None:
    tomorrow = datetime.now(timezone.utc) + timedelta(days=1)

    if start_date < tomorrow:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Start date must be at least 1 day in the future")


def unique_teams_in_tournament(teams: list[str]) -> None:
    if len(teams) != len(set(teams)):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="There is a duplicate team in the tournament list")