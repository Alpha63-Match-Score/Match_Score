from datetime import datetime, timezone
from typing import Optional, List, ForwardRef
from uuid import UUID
from pydantic import BaseModel, Field, field_validator, EmailStr, validator
from src.models.enums import TournamentFormat, Stage, MatchFormat, RequestType, RequestStatus

# Forward References
PlayerListResponse = ForwardRef('PlayerListResponse')
TeamListResponse = ForwardRef('TeamListResponse')
MatchListResponse = ForwardRef('MatchListResponse')
TournamentListResponse = ForwardRef('TournamentListResponse')
PrizeCutResponse = ForwardRef('PrizeCutResponse')


# Base configs
class BaseConfig(BaseModel):
    model_config = {
        "from_attributes": True
    }


# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_identifier: int | None = None
    user_email: str | None = None


# User schemas
class UserBase(BaseConfig):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(
        min_length=4,
        max_length=36,
        examples=["Example123@"]
    )

    @field_validator('password')
    def validate_password(cls, value):
        if not (
            any(c.isupper() for c in value) and
            any(c.islower() for c in value) and
            any(c.isdigit() for c in value) and
            any(c in '@$!%*?&' for c in value) and
            not any(c.isspace() for c in value)
        ):
            raise ValueError(
                "Password must contain at least one uppercase letter, one lowercase letter, "
                "one number, one special character, and must not contain any spaces"
            )
        return value


class UserResponse(UserBase):
    id: UUID
    email: EmailStr
    role: str


class UserRegisterResponse(BaseConfig):
    email: EmailStr
    role: str


class UserUpdate(UserBase):
    pass


# Player schemas
class PlayerListResponse(BaseConfig):
    id: UUID
    first_name: str
    last_name: str
    country: str

class PlayerDetailResponse(PlayerListResponse):
    avatar: str | None
    team_id: UUID
    tournaments: List["TournamentListResponse"]

class PlayerCreate(BaseConfig):
    username: str = Field(
        min_length=5,
        max_length=15,
        pattern="^[a-zA-Z0-9_-]+$",
        examples=["example_user"]
    )
    first_name: str = Field(
        min_length=2,
        max_length=25,
        pattern="^[a-zA-Z]+(?:-[a-zA-Z]+)?$",
        examples=["Example"]
    )
    last_name: str = Field(
        min_length=2,
        max_length=25,
        pattern="^[a-zA-Z]+(?:-[a-zA-Z]+)?$",
        examples=["Example"]
    )
    country: str = Field(
        min_length=2,
        max_length=25,
        pattern="^[a-zA-Z]+(?:-[a-zA-Z]+)?$",
        examples=["Example"]
    )
    avatar: Optional[str]
    user_id: UUID | None = None
    team_id: UUID | None = None

    @field_validator('first_name', 'last_name', mode='before')
    def capitalize_names(cls, value):
        return '-'.join(part.capitalize() for part in value.split('-'))

class PlayerUpdate(BaseConfig):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    country: str | None = None
    avatar: str | None = None
    user_id: UUID | None = None
    team_id: UUID | None = None

    @field_validator('first_name', 'last_name', mode='before')
    def capitalize_names(cls, value):
        return '-'.join(part.capitalize() for part in value.split('-'))


# Team schemas
class TeamListResponse(BaseConfig):
    id: UUID
    name: str
    logo: str | None

class TeamDetailedResponse(BaseConfig):
    players: List[PlayerListResponse]
    #TODO: Please add these (needed for front-end):
    # matches: List[MatchListResponse]
    # tournament_id: UUID
    # prize_cuts: List[PrizeCutResponse]
    # ratings/statistics?


class TeamCreate(BaseConfig):
    # id: UUID
    name: str  = Field(
        min_length=5,
        max_length=15,
        pattern="^[a-zA-Z0-9_-]+$",
        examples=["example_team"]
    )
    logo: Optional[str]

class TeamUpdate(BaseConfig):
    name: str | None = None
    logo: str | None = None

# Match schemas
class MatchListResponse(BaseConfig):
    id: UUID
    match_format: MatchFormat
    start_time: datetime
    is_finished: bool
    stage: Stage
    team1_id: UUID
    team2_id: UUID
    team1_score: int
    team2_score: int
    winner_id: UUID | None = None
    tournament_id: UUID

class MatchDetailResponse(MatchListResponse):
   team1_name: str
   team2_name: str
   team1_logo: str | None = None
   team2_logo: str | None = None
   tournament_title: str

class MatchUpdate(BaseConfig):
    start_time: datetime | None = None
    stage: Stage | None = None
    team1_id: UUID | None = None
    team2_id: UUID | None = None


# Tournament schemas
class TournamentListResponse(BaseConfig):
    id: UUID
    title: str
    tournament_format: TournamentFormat
    start_date: datetime
    end_date: datetime
    current_stage: Stage
    number_of_teams: int | None = None

class TournamentDetailResponse(TournamentListResponse):
    matches_of_current_stage: List[MatchListResponse]
    teams: List[TeamListResponse]
    prizes: List[PrizeCutResponse]


class TournamentCreate(BaseConfig):
   title: str = Field(
        min_length=3,
        max_length=50,
        examples=["Example Tournament Title"]
    )
   tournament_format: TournamentFormat
   start_date: datetime
   team_names: List[str]
   prize_pool: int = Field(
        ge=1,
        examples=[1000])


class TournamentUpdate(BaseConfig):
   title: str | None = None, Field(
        min_length=3,
        max_length=20,
        pattern="^[a-zA-Z0-9_-]+$",
        examples=["Example Tournament Title"]
    )
   start_date: datetime | None = None
   end_date: datetime | None = None
   prize_pool: int | None = None

# PrizeCut schemas
class PrizeCutResponse(BaseConfig):
    id: UUID
    place: int
    prize_cut: float
    tournament_id: UUID
    tournament_name: str
    team_id: UUID | None
    team_name: str | None

class PrizeCutUpdate(BaseConfig):
    team_id: UUID

# Request schemas
class RequestBase(BaseConfig):
    response_date: Optional[str] = None
    user_id: UUID
    request_type: RequestType
    player_id: Optional[UUID] = None
    admin_id: Optional[UUID] = None


# class LinkUserToPlayer(BaseConfig):
#     player_id: UUID
#     admin_id: UUID
#     request_type: RequestType = RequestType.LINK_USER_TO_PLAYER
#     status: RequestStatus
    # response_date: datetime = datetime.now()


class ResponseRequest(BaseConfig):
    request_type: RequestType = RequestType.PROMOTE_USER_TO_DIRECTOR
    status: RequestStatus
    request_date: datetime
    # response_date: datetime = datetime.now()


class RequestListResponse(BaseConfig):
    request_type: RequestType
    status: RequestStatus
    request_date: datetime
    admin_id: UUID | None


# Updating forward references
PlayerListResponse.model_rebuild()
TournamentDetailResponse.model_rebuild()
TeamDetailedResponse.model_rebuild()