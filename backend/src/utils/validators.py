from datetime import datetime, timedelta, timezone
from typing import Type
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models import Match, Player, Request, Tournament, User
from src.models.enums import Role, Stage
from src.models.team import Team
from src.schemas.user import UserResponse
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)


# existing validators
def tournament_exists(
    db: Session, tournament_id: UUID | None = None, tournament_title: str | None = None
) -> Type[Tournament]:

    tournament = None
    if tournament_id:
        tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    elif tournament_title:
        tournament = (
            db.query(Tournament).filter(Tournament.title == tournament_title).first()
        )

    if not tournament:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Tournament not found"
        )

    return tournament


def team_exists(
    db: Session,
    team_id: UUID | None = None,
    team_name: str | None = None,
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


def user_exists(
    db: Session,
    user_id: UUID | None = None,
    user_email: str | None = None,
) -> Type[User]:
    user = None

    if user_id:
        user = db.query(User).filter(User.id == user_id).first()
    if user_email:
        user = db.query(User).filter(User.email == user_email).first()

    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

    return user


def request_exists(db: Session, request_id: UUID) -> Type[Request]:
    request = db.query(Request).filter(Request.id == request_id).first()
    if not request:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Request not found.")

    return request


def player_exists(
    db: Session, player_id: UUID | None = None, username: str | None = None
) -> Type[Player]:

    player = None
    if player_id:
        player = db.query(Player).filter(Player.id == player_id).first()
    else:
        player = db.query(Player).filter(Player.username == username).first()

    if not player:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Player not found")

    return player


def player_username_unique(db: Session, username: str) -> None:
    if db.query(Player).filter(Player.username == username).first():
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Player with this username already exists",
        )


def team_name_unique(db: Session, team_name: str) -> None:
    if db.query(Team).filter(Team.name == team_name).first():
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Team '{team_name}' already exists",
        )


def player_already_linked(db: Session, username: str) -> None:
    player = db.query(Player).filter(Player.username == username).first()
    if player and player.user_id:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Player is already linked to a user.",
        )


def user_email_exists(db: Session, email: str) -> None:
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Email already exists"
        )


def tournament_title_unique(db: Session, title: str) -> None:
    if db.query(Tournament).filter(Tournament.title == title).first():
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Tournament with this title already exists",
        )


# authorisation validators
def director_or_admin(user: UserResponse) -> None:
    if user.role not in [Role.DIRECTOR, Role.ADMIN]:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action",
        )


def is_author_of_tournament(db: Session, tournament_id: UUID, user_id: UUID) -> None:
    db_tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if db_tournament.director_id != user_id:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action",
        )


def user_role_is_admin(current_user: User) -> None:
    if current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Only admins can perform this action.",
        )


def user_role_is_user(current_user: User) -> None:
    if current_user.role != Role.USER:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Only users can send requests."
        )


def player_update_current_user_authorization(db_player, current_user) -> None:
    if db_player.user_id != current_user.id and current_user.role != Role.ADMIN:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this player",
        )


# datetime validators
def validate_start_date(start_date) -> None:
    tomorrow = datetime.now(timezone.utc) + timedelta(days=1)

    if start_date < tomorrow:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Start date must be at least 1 day in the future",
        )


def validate_old_vs_new_end_date(old_end_date, new_end_date) -> None:
    old_end_date = old_end_date.replace(tzinfo=timezone.utc)
    new_end_date = new_end_date.replace(tzinfo=timezone.utc)
    if old_end_date > new_end_date:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"New end date must be after "
            f"{old_end_date.strftime('%Y-%m-%d %H:%M:%S')}",
        )


def unique_teams_in_tournament(teams: list[str]) -> None:
    if len(teams) != len(set(teams)):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="There is a duplicate team in the tournament list",
        )


# state of match
def match_is_finished(match: Type[Match]) -> None:
    if match.is_finished:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Match is already finished"
        )


def match_has_started(match: Type[Match]) -> None:
    match_start = match.start_time.replace(tzinfo=timezone.utc)
    if (match.team1_score > 0 or match.team2_score > 0) or (
        match_start < datetime.now(timezone.utc)
    ):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Match has already started"
        )


def team_has_five_players(team: Type[Team]) -> None:
    if len(team.players) != 5:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Team '{team.name}' must have 5 players",
        )


# state of tournament
def tournament_is_finished(tournament: Type[Tournament]) -> None:
    tournament_end = tournament.end_date.replace(tzinfo=timezone.utc)
    if (tournament.current_stage == Stage.FINISHED) or (
        tournament_end < datetime.now(timezone.utc)
    ):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Tournament is already finished"
        )


def tournament_has_started(tournament: Type[Tournament]) -> None:
    tournament_start = tournament.start_date.replace(tzinfo=timezone.utc)
    flag = False
    for match in tournament.matches:
        if match.team1_score != 0 or match.team2_score != 0:
            flag = True

    if (tournament_start < datetime.now(timezone.utc)) or flag:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Tournament has already started"
        )


def team_player_limit_reached(team: Type[Team]) -> None:
    if len(team.players) == 10:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Team has reached the player limit"
        )


def user_associated_with_player(user: User) -> None:
    if user.role != Role.PLAYER:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="User does not have associated player",
        )
