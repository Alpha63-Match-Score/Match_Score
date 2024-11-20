from typing import Type
from uuid import UUID

from dns.e164 import query
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST
from src.utils import validators as v
from src.models import Tournament
from src.models.team import Team
from src.schemas.schemas import TeamListResponse, TeamCreate, UserResponse
from src.utils import validators as v
from src.utils.pagination import PaginationParams


def get_teams(db: Session,
              pagination: PaginationParams,
              search: str | None = None) -> TeamListResponse:

    query = db.query(Team).order_by(Team.name.asc())

    filters = []

    if search:
        filters.append(Team.name.ilike(f"%{search}%"))

    if filters:
        query = db.query(Team).filter(*filters)

    query = query.offset(pagination.offset).limit(pagination.limit)

    db_teams = query.all()
    return [convert_db_to_team_list_response(db_team) for db_team in db_teams]

def create_team( db: Session, team: TeamCreate, current_user: UserResponse)-> TeamListResponse:
    # v.team_exists(db, team_name=team.name)
    v.director_or_admin(current_user)

    db_team = Team(
        name=team.name,
        logo=team.logo,
 )

    db.add(db_team)
    db.commit()
    db.refresh(db_team)

    return convert_db_to_team_list_response(db_team)


def convert_db_to_team_list_response(
        db_team: Type[Team]
) -> TeamListResponse:
    return TeamListResponse(
        id=db_team.id,
        name=db_team.name,
        logo=db_team.logo,
    )


def create_teams_lst_for_tournament(
        db: Session,
        team_names: list[str],
        tournament_id: UUID
) -> None:

    teams = []
    for name in team_names:
        db_team = v.team_exists(db, team_name=name)

        if db_team.tournament_id is not None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f"Team '{db_team.name}' already participates in another tournament")

        if len(db_team.players) < 5:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Team must have at least 5 players")

        teams.append(db_team)

    for db_team in teams:
        db_team.tournament_id = tournament_id


def leave_top_teams_from_robin_round(
        db_tournament: Type[Tournament],
) -> None:

    team_stats = {}
    for match in db_tournament.matches:
            if match.winner_team_id not in team_stats:
                team_stats[match.winner_team] = 0
            team_stats[match.winner_team] += 1

    top_scores = sorted(team_stats.values(), reverse=True)[:2]

    best_teams = []
    for team, score in team_stats.items():
        if score in top_scores:
            best_teams.append(team)
        else:
            team.tournament_id = None