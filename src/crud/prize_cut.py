from typing import Type

from src.models import PrizeCut
from src.schemas.schemas import PrizeCutResponse


def convert_db_to_prize_cut_response(
        db_prize: PrizeCut | Type[PrizeCut]
) -> PrizeCutResponse:

    return PrizeCutResponse(
        id=db_prize.id,
        place=db_prize.place,
        prize_cut=db_prize.prize_cut,
        tournament_id=db_prize.tournament_id,
        team_id=db_prize.team_id,
        team_name=db_prize.team.name if db_prize.team else None
    )