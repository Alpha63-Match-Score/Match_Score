from datetime import datetime, timezone
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from src.models import Tournament, Match, User
from src.models.enums import Stage, Role, TournamentFormat, MatchFormat
from src.models.team import Team
from src.schemas.schemas import UserResponse


def tournament_exists(db: Session, tournament_id: UUID) -> None:
    if not db.query(Tournament).filter(Tournament.id == tournament_id).first():
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Tournament not found")

def team_exists(db: Session, team_id: UUID) -> None:
    if not db.query(Team).filter(Team.id == team_id).first():
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Team not found")

def team_exists_by_name(db: Session, team_name: str) -> None:
    if not db.query(Team).filter(Team.name == team_name).first():
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Team not found")

def match_exists(db: Session, match_id: UUID) -> None:
    if not db.query(Match).filter(Match.id == match_id).first():
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Match not found")

def user_exists(db: Session, user_id: UUID) -> None:
    if not db.query(User).filter(User.id == user_id).first():
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")

def stage_exists(stage: Stage) -> None:
    if stage not in Stage:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid stage")

def director_or_admin(user: UserResponse) -> None:
    if user.role not in [Role.DIRECTOR, Role.ADMIN]:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="User is not authorized to perform this action")

def validate_start_time(start_time) -> None:
    if start_time < datetime.now():
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Start time must be in the future")

def validate_start_vs_end_date(start_date, end_date) -> None:
    now = datetime.now(timezone.utc)

    if start_date < now:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Start date must be in the future")
    if end_date < start_date:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="End must be after start")

def tournament_title_unique(db: Session, title: str) -> None:
    if db.query(Tournament).filter(Tournament.title == title).first():
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Tournament title must be unique")

def tournament_format_number_of_teams(tournament_format: str, number_of_teams: int) -> Stage:
    if tournament_format == TournamentFormat.SINGLE_ELIMINATION:
        if number_of_teams not in [4, 8, 16]:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Invalid number of teams for single elimination - must be 4, 8 or 16")
        if number_of_teams == 4:
            return Stage.SEMI_FINAL
        elif number_of_teams == 8:
            return Stage.QUARTER_FINAL
        else:
            return Stage.ROUND_OF_16

    elif tournament_format == TournamentFormat.ROUND_ROBIN:
        if number_of_teams not in [4, 5]:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Invalid number of teams for round robin - must be 4 or 5")
        return Stage.GROUP_STAGE

    elif tournament_format == TournamentFormat.ONE_OFF_MATCH:
        if number_of_teams != 2:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Invalid number of teams for one off match - must be 2")
        return Stage.FINAL

def is_author_of_tournament(db: Session, tournament_id: UUID, user_id: UUID) -> None:
    db_tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()
    if db_tournament.director_id != user_id:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="You are not authorized to perform this action")
