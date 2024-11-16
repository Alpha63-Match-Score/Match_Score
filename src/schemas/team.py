from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

from src.schemas.player import PlayerListResponse


class TeamCreate(BaseModel):
    id: UUID
    name: str  = Field(
        min_length=5,
        max_length=15,
        pattern="^[a-zA-Z0-9_-]+$",
        examples=["example_team"]
    )
    logo: Optional[str]
    played_games: int
    won_games: int

class TeamUpdate(BaseModel):
    name: str | None = None
    logo: str | None = None
    played_games: int | None = None
    won_games: int | None = None

class TeamListResponse(BaseModel):
    name: str
    logo: str

class TeamDetailedListResponse(BaseModel):
    id: UUID
    played_games: int
    won_games: int
    players: list[PlayerListResponse]