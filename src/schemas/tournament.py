from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from src.models.enums import TournamentFormat, Stage
from src.schemas.match import MatchListResponse
from src.schemas.prize_cut import PrizeCutResponse


class TournamentListResponse(BaseModel):
    id: UUID
    match_format: TournamentFormat
    start_date: datetime
    end_date: datetime
    prize_pool: int
    current_stage: Stage
    director_id: UUID

class TournamentDetailResponse(TournamentListResponse):
    matches: list[MatchListResponse]
    prizes: list[PrizeCutResponse]

class TournamentCreate(BaseModel):
   title: str
   tournament_format: TournamentFormat
   start_date: datetime
   end_date: datetime
   prize_pool: int
   director_id: UUID

class TournamentUpdate(BaseModel):
   title: str | None = None
   start_date: datetime | None = None
   end_date: datetime | None = None
   prize_pool: int | None = None
   current_round: Stage | None = None

