from datetime import datetime
from http.client import HTTPException
from typing import Literal, Type
from uuid import UUID

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.crud.match import convert_db_to_match_list_response
from src.crud.prize_cut import convert_db_to_prize_cut_response
from src.models import Tournament, Team
from src.models.enums import Stage
from src.schemas.schemas import TournamentListResponse, TournamentDetailResponse, TeamListResponse
from src.utils.pagination import PaginationParams
from src.utils import validators as v


def get_tournaments(
    db: Session,
    pagination: PaginationParams,
    period: Literal['past', 'present', 'future'] | None = None,
    search: str | None = None,
    director_id: UUID | None = None,
) -> list[TournamentListResponse]:

    query = db.query(Tournament).order_by(Tournament.start_date.asc())

    filters = []

    if period:
        if period == 'past':
            filters.append(Tournament.end_date < datetime.now())
        elif period == 'present':
            filters.append(
                and_(Tournament.start_date <= datetime.now(),
                     Tournament.end_date >= datetime.now()))
        elif period == 'future':
            filters.append(Tournament.start_date > datetime.now())

    if search:
        filters.append(Tournament.title.ilike(f"%{search}%"))

    if director_id:
        v.user_exists(db, director_id)
        filters.append(Tournament.director_id == director_id)

    if filters:
        query = query.filter(*filters)

    query = query.offset(pagination.skip).limit(pagination.limit)

    db_tournaments = query.all()

    all_tournaments = []
    for db_tournament in db_tournaments:
        participants = len(db_tournament.matches) * 2 if db_tournament.matches else 0
        all_tournaments.append(convert_db_to_tournament_list_response(db_tournament, participants))

    return all_tournaments

def get_tournament(
    db: Session,
    tournament_id: UUID
) -> TournamentListResponse:

    v.tournament_exists(db, tournament_id)
    db_tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()

    participants = []
    for db_match in db_tournament.matches:
        if db_match.team1_id not in participants:
            participants.append(db_match.team1)
        if db_match.team2_id not in participants:
            participants.append(db_match.team2)

    return convert_db_to_tournament_response(db_tournament, participants)


def convert_db_to_tournament_list_response(
        db_tournament: Tournament | Type[Tournament],
        participants: int
) -> TournamentListResponse:

    return TournamentListResponse(
        id=db_tournament.id,
        title=db_tournament.title,
        tournament_format=db_tournament.tournament_format,
        start_date=db_tournament.start_date,
        end_date=db_tournament.end_date,
        current_stage=db_tournament.current_stage,
        number_of_participants=participants
    )

def convert_db_to_tournament_response(
        db_tournament: Tournament | Type[Tournament],
        participants: list[Team]
) -> TournamentDetailResponse:

    return TournamentDetailResponse(
        id=db_tournament.id,
        title=db_tournament.title,
        tournament_format=db_tournament.tournament_format,
        start_date=db_tournament.start_date,
        end_date=db_tournament.end_date,
        current_stage=db_tournament.current_stage,
        number_of_participants=len(db_tournament.matches) * 2 if db_tournament.matches else 0,
        matches=[convert_db_to_match_list_response(db_match) for db_match in db_tournament.matches],
        participants=[convert_db_to_team_list_response(team) for team in participants],
        prizes=[convert_db_to_prize_cut_response(db_prize) for db_prize in db_tournament.prize_cuts]
    )

def convert_db_to_team_list_response(
        db_team: Team
) -> TeamListResponse:

        return TeamListResponse(
            name=db_team.name,
            logo=db_team.logo,
        )
