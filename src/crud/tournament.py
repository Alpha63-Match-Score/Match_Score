from typing import Literal, Type
from uuid import UUID

from sqlalchemy.orm import Session

from src.models import Tournament
from src.models.enums import Stage
from src.schemas.tournament import TournamentListResponse
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

    if pagination.skip:
        query = query.offset(pagination.skip)
    if pagination.limit:
        query = query.limit(pagination.limit)
    if period:
        filters.append(Tournament.start_date == period)
    if search:
        filters.append(Tournament.title.ilike(f"%{search}%"))
    if director_id:
        v.user_exists(db, director_id)
        filters.append(Tournament.director_id == director_id)

    if filters:
        query = query.filter(*filters)

    db_tournaments = query.all()

    all_tournaments = []
    for db_tournament in db_tournaments:
        current_stage = db_tournament.matches[-1].stage
        participants = len(db_tournament.matches) * 2
        all_tournaments.append(_convert_db_to_tournament_list_response(db_tournament, current_stage, participants))

    return all_tournaments


def _convert_db_to_tournament_list_response(
        db_tournament: Tournament | Type[Tournament],
        current_stage: Stage,
        participants: int
) -> TournamentListResponse:

    return TournamentListResponse(
        id=db_tournament.id,
        title=db_tournament.title,
        tournament_format=db_tournament.tournament_format,
        start_date=db_tournament.start_date,
        end_date=db_tournament.end_date,
        current_stage=current_stage,
        number_of_participants=participants
    )
