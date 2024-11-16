# from datetime import datetime
# from uuid import UUID
# from pydantic import BaseModel, Field
#
# from src.models.enums import TournamentFormat, Stage
# from src.schemas.match import MatchListResponse
# from src.schemas.prize_cut import PrizeCutResponse
# from src.schemas.team import TeamListResponse
#
# class TournamentBase(BaseModel):
#     class Config:
#         orm_mode = True
#
# class TournamentListResponse(TournamentBase):
#     id: UUID
#     title: str = Field(
#         min_length=3,
#         max_length=20,
#         pattern="^[a-zA-Z0-9_-]+$",
#         examples=["Example Tournament Title"]
#     )
#     tournament_format: TournamentFormat
#     start_date: datetime
#     end_date: datetime
#     current_stage: Stage
#     number_of_participants: int
#
# class TournamentDetailResponse(TournamentListResponse):
#     matches: list[MatchListResponse]
#     participants: list[TeamListResponse]
#     prizes: list[PrizeCutResponse]
#
# class TournamentCreate(TournamentBase):
#    title: str = Field(
#         min_length=3,
#         max_length=20,
#         pattern="^[a-zA-Z0-9_-]+$",
#         examples=["Example Tournament Title"]
#     )
#    tournament_format: TournamentFormat
#    start_date: datetime
#    end_date: datetime
#    prize_pool: int
#    director_id: UUID
#
# class TournamentUpdate(TournamentBase):
#    title: str | None = Field(
#         min_length=3,
#         max_length=20,
#         pattern="^[a-zA-Z0-9_-]+$",
#         examples=["Example Tournament Title"]
#     )
#    start_date: datetime | None = None
#    end_date: datetime | None = None
#    prize_pool: int | None = None
#    current_round: Stage | None = None
#
