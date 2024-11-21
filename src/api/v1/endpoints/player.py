
from src.api.deps import get_current_user, get_db
from src.crud import player as player_crud
from src.schemas.schemas import (
    PlayerCreate,
    PlayerDetailResponse,
    PlayerListResponse,
    PlayerUpdate,
    UserResponse,
)
from src.utils.pagination import PaginationParams, get_pagination

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/", response_model=PlayerListResponse, status_code=201)
def create_player(
    team: PlayerCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return player_crud.create_player(db, team, current_user)


@router.get("/")
def get_players(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(get_pagination),
    search: str | None = None,
):
    return player_crud.get_players(db, pagination, search)


@router.get("/{player_username}", response_model=PlayerDetailResponse, status_code=201)
def get_player(player_username: str, db: Session = Depends(get_db)):
    return player_crud.get_player(db, player_username)


@router.put("/{player_username}", response_model=PlayerListResponse, status_code=201)
def update_player(
    player_username: str,
    player: PlayerUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return player_crud.update_player(db, player_username, player, current_user)
