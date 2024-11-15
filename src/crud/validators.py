from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from src.models import Tournament, Match, Team
from src.models.enums import Stage, Role


def tournament_exists(db: Session, tournament_id: UUID) -> None:
    if not db.query(Tournament).filter(Tournament.id == tournament_id).first():
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Tournament not found")

def team_exists(db: Session, team_id: UUID) -> None:
    if not db.query(Team).filter(Team.id == team_id).first():
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Team not found")

def match_exists(db: Session, match_id: UUID) -> None:
    if not db.query(Match).filter(Match.id == match_id).first():
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Match not found")

def stage_exists(stage: Stage) -> None:
    if stage not in Stage:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid stage")

def director_or_admin(user) -> None:
    if user.role not in [Role.DIRECTOR, Role.ADMIN]:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="User is not authorized to perform this action")