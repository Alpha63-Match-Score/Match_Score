from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from src.models.enums import TournamentFormat
from src.schemas.match import MatchListResponse


class TournamentListResponse(BaseModel):
    id: UUID
    title: str
    tournament_format: TournamentFormat
    start_date: datetime
    end_date: datetime
    prize_pool: int
    director_id: UUID

class TournamentDetailResponse(TournamentListResponse):
    matches: list[MatchListResponse]

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

