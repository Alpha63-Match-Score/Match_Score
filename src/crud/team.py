from typing import Type
from uuid import UUID

from src.models import Tournament
from src.models.team import Team
from src.schemas.schemas import TeamCreate, TeamListResponse, UserResponse
from src.utils import validators as v
from src.utils.pagination import PaginationParams

from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST


def get_teams(
    db: Session, pagination: PaginationParams, search: str | None = None
) -> TeamListResponse:

    query = db.query(Team).order_by(Team.name.asc())

    filters = []

    if search:
        filters.append(Team.name.ilike(f"%{search}%"))

    if filters:
        query = db.query(Team).filter(*filters)

    query = query.offset(pagination.offset).limit(pagination.limit)

    db_teams = query.all()
    return [convert_db_to_team_list_response(db_team) for db_team in db_teams]


def create_team(
    db: Session, team: TeamCreate, current_user: UserResponse
) -> TeamListResponse:
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


def convert_db_to_team_list_response(db_team: Type[Team]) -> TeamListResponse:
    return TeamListResponse(
        id=db_team.id,
        name=db_team.name,
        logo=db_team.logo,
    )


def create_teams_lst_for_tournament(
    db: Session, team_names: list[str], tournament_id: UUID
) -> None:

    teams = []
    for name in team_names:
        db_team = db.query(Team).filter(Team.name == name).first()

        if db_team is None:
            new_team = Team(name=name)
            db.add(new_team)
            db.flush()
            teams.append(new_team)
        else:
            if db_team.tournament_id is not None:
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST,
                    detail=f"Team '{db_team.name}' already participates in another tournament",
                )

            teams.append(db_team)

    for db_team in teams:
        db_team.tournament_id = tournament_id


def leave_top_teams_from_robin_round(db, db_tournament: Tournament) -> None:
    team_stats = {}
    for team in db_tournament.teams:
        team_stats[team] = {
            "points": 0,
            "wins": 0,
            "score_difference": 0,
            "total_score": 0,
        }

    for match in db_tournament.matches:
        team1 = match.team1
        team2 = match.team2

        team_stats[team1]["total_score"] += match.team1_score
        team_stats[team2]["total_score"] += match.team2_score

        team_stats[team1]["score_difference"] += match.team1_score - match.team2_score
        team_stats[team2]["score_difference"] += match.team2_score - match.team1_score

        winner = team1 if match.winner_team_id == team1.id else team2
        team_stats[winner]["points"] += 2
        team_stats[winner]["wins"] += 1

    sorted_teams = sorted(
        team_stats.keys(),
        key=lambda t: (
            team_stats[t]["points"],
            team_stats[t]["wins"],
            team_stats[t]["score_difference"],
            team_stats[t]["total_score"],
        ),
        reverse=True,
    )

    for team in sorted_teams[2:]:
        team.tournament_id = None

    db.flush()
