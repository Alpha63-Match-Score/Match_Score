from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from src.api.deps import get_current_user, get_db
from src.crud import team as team_crud
from src.schemas.team import (
    TeamCreate,
    TeamDetailedResponse,
    TeamListResponse,
    TeamUpdate,
)
from src.schemas.user import UserResponse
from src.utils.pagination import PaginationParams, get_pagination

router = APIRouter()


@router.get("/")
def get_teams(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(get_pagination),
    search: str | None = None,
    is_available: Literal["true", "false"] | None = None,
    has_space: Literal["true", "false"] | None = None,
    sort_by: Literal["asc", "desc"] = "asc",
):
    return team_crud.get_teams(db, pagination, search, is_available, has_space, sort_by)


@router.get("/{team_id}", response_model=TeamDetailedResponse)
def get_team(team_id: UUID, db: Session = Depends(get_db)):
    return team_crud.get_team(db, team_id)


@router.post("/", response_model=TeamListResponse, status_code=201)
def create_team(
    team: TeamCreate = Depends(),
    logo: UploadFile | str = File(None),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return team_crud.create_team(db, team, logo, current_user)


@router.put("/{team_id}", response_model=TeamListResponse)
def update_team(
    team_id: UUID,
    team: TeamUpdate = Depends(),
    logo: UploadFile | str = File(None),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return team_crud.update_team(db, team_id, team, logo, current_user)
