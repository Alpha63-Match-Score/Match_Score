from src.api.deps import get_current_user, get_db
from src.crud import team as team_crud
from src.schemas.schemas import TeamCreate, TeamListResponse, UserResponse, TeamDetailedResponse, TeamUpdate
from src.utils.pagination import PaginationParams, get_pagination

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

router = APIRouter()


@router.get("/")
def get_teams(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(get_pagination),
    search: str | None = None,
):
    return team_crud.get_teams(db, pagination, search)


@router.get("/{team_id}", response_model=TeamDetailedResponse, status_code = 201)
def get_team(team_id: UUID, db: Session = Depends(get_db)):
    return team_crud.get_team(db, team_id)


@router.post("/", response_model=TeamListResponse, status_code=201)
def create_team(
    team: TeamCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return team_crud.create_team(db, team, current_user)


@router.put("/{team_id}", response_model=TeamListResponse, status_code = 201)
def update_team(team_id: UUID, team: TeamUpdate, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    return team_crud.update_team(db, team_id, team, current_user)