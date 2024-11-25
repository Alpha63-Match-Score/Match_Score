from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from src.api.deps import get_current_user, get_db
from src.crud import team as team_crud
from src.schemas.schemas import (
    TeamCreate,
    TeamDetailedResponse,
    TeamListResponse,
    TeamUpdate,
    UserResponse,
)
from src.utils.pagination import PaginationParams, get_pagination

router = APIRouter()


@router.get("/")
def get_teams(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(get_pagination),
    search: str | None = None,
    sort_by: Literal["asc", "desc"] = "asc",
):
    return team_crud.get_teams(db, pagination, search, sort_by)


@router.get("/{team_id}", response_model=TeamDetailedResponse)
def get_team(team_id: UUID, db: Session = Depends(get_db)):
    return team_crud.get_team(db, team_id)


@router.post("/", response_model=TeamListResponse, status_code=201)
def create_team(
    team: TeamCreate,
    logo: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return team_crud.create_team(db, team, logo, current_user)


@router.put("/{team_id}", response_model=TeamListResponse)
def update_team(
    team_id: UUID,
    team: TeamUpdate,
    logo: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return team_crud.update_team(db, team_id, team, logo, current_user)
