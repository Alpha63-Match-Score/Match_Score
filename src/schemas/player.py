# from pydantic import BaseModel, Field, field_validator
# from uuid import UUID
# from typing import Optional
#
# from src.schemas.schemas import TournamentListResponse
#
#
# class PlayerCreate(BaseModel):
#     id: UUID
#     username: str = Field(
#         min_length=5,
#         max_length=15,
#         pattern="^[a-zA-Z0-9_-]+$",
#         examples=["example_user"]
#     )
#     first_name: str = Field(
#         min_length=2,
#         max_length=25,
#         pattern="^[a-zA-Z]+(?:-[a-zA-Z]+)?$",
#         examples=["Example"]
#     )
#     last_name: str = Field(
#         min_length=2,
#         max_length=25,
#         pattern="^[a-zA-Z]+(?:-[a-zA-Z]+)?$",
#         examples=["Example"]
#     )
#     country: str = Field(
#         min_length=2,
#         max_length=25,
#         pattern="^[a-zA-Z]+(?:-[a-zA-Z]+)?$",
#         examples=["Example"]
#     )
#     avatar: Optional[str]
#     played_games: int
#     won_games: int
#     user_id: UUID | None = None
#     team_id: UUID | None = None
#
#     @field_validator('first_name', 'last_name', mode='before')
#     def capitalize_names(cls, value):
#         return '-'.join(part.capitalize() for part in value.split('-'))
#
#
# class PlayerUpdate(BaseModel):
#     username: str | None = None
#     first_name: str | None = None
#     last_name: str | None = None
#     country: str | None = None
#     avatar: str | None = None
#     played_games: int | None = None
#     won_games: int | None = None
#     user_id: UUID | None = None
#     team_id: UUID | None = None
#
#     @field_validator('first_name', 'last_name', mode='before')
#     def capitalize_names(cls, value):
#         return '-'.join(part.capitalize() for part in value.split('-'))
#
# class PlayerListResponse(BaseModel):
#     first_name: str
#     last_name: str
#     country: str
#
#
# class PlayerDetailResponse(PlayerListResponse):
#     played_games: int
#     won_games: int
#     avatar: str
#     team_id: UUID
#     tournaments: list[TournamentListResponse]