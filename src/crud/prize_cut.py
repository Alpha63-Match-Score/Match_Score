from typing import Type
from uuid import UUID

from pydantic.v1 import UUID1

from src.models import PrizeCut
from src.schemas.schemas import PrizeCutResponse


def create_prize_cuts_for_tournament(
        db,
        db_tournament,
) -> None:

    prize_cut1 = _create_prize_cut(1, 0.7 * db_tournament.prize_pool, db_tournament.id)
    prize_cut2 = _create_prize_cut(2, 0.3 * db_tournament.prize_pool, db_tournament.id)

    db.add(prize_cut1)
    db.add(prize_cut2)

    db.commit()
    db.refresh(prize_cut1)
    db.refresh(prize_cut2)

def _create_prize_cut(
        place: int,
        prize_cut: int,
        tournament_id: UUID,
) -> PrizeCut:

    db_prize = PrizeCut(
        place=place,
        prize_cut=prize_cut,
        tournament_id=tournament_id,
        team_id=None
    )

    return db_prize

def convert_db_to_prize_cut_response(
        db_prize: PrizeCut | Type[PrizeCut]
) -> PrizeCutResponse:

    return PrizeCutResponse(
        id=db_prize.id,
        place=db_prize.place,
        prize_cut=db_prize.prize_cut,
        tournament_id=db_prize.tournament_id,
        tournament_name=db_prize.tournament.title,
        team_id=db_prize.team_id,
        team_name=db_prize.team.name if db_prize.team else None
    )