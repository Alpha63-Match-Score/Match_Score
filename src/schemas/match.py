# from datetime import datetime
# from uuid import UUID
# from pydantic import BaseModel
#
# from src.models.enums import Stage, MatchFormat
#
# class MatchBase(BaseModel):
#
#     class Config:
#         orm_mode = True
#
# class MatchListResponse(MatchBase):
#     id: UUID
#     match_format: MatchFormat
#     start_time: datetime
#     is_finished: bool
#     stage: Stage
#     team1_id: UUID
#     team2_id: UUID
#     team1_score: int
#     team2_score: int
#     tournament_id: UUID
#
# class MatchDetailResponse(MatchListResponse):
#    team1_name: str
#    team2_name: str
#    team1_logo: str
#    team2_logo: str
#    tournament_title: str
#
# class MatchCreate(MatchBase):
#     match_format: MatchFormat
#     start_time: datetime
#     stage: Stage
#     team1_id: UUID
#     team2_id: UUID
#     tournament_id: UUID
#
# class MatchUpdate(MatchBase):
#     start_time: datetime | None = None
#     is_finished: bool | None = None
#     stage: Stage | None = None
#     team1_score: int | None = None
#     team2_score: int | None = None
#
