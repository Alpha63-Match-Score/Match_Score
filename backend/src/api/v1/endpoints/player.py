from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from src.api.deps import get_current_user, get_db
from src.crud import player as player_crud
from src.schemas.player import (
    PlayerCreate,
    PlayerDetailResponse,
    PlayerListResponse,
    PlayerUpdate
)
from src.schemas.user import UserResponse
from src.utils.pagination import PaginationParams, get_pagination

router = APIRouter()


@router.post("/", response_model=PlayerListResponse, status_code=201)
def create_player(
    player: PlayerCreate = Depends(),
    avatar: UploadFile | str = File(None),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return player_crud.create_player(db, player, avatar, current_user)


@router.get("/")
def get_players(
    db: Session = Depends(get_db),
    pagination: PaginationParams = Depends(get_pagination),
    search: str | None = None,
    team: str | None = None,
    country: str | None = None,
    sort_by: Literal["asc", "desc"] = "asc",
):
    return player_crud.get_players(
        db, pagination, search, team, country, sort_by
    )


@router.get("/{player_id}", response_model=PlayerDetailResponse)
def get_player(player_id: UUID, db: Session = Depends(get_db)):
    return player_crud.get_player(db, player_id)


@router.put("/{player_id}", response_model=PlayerListResponse)
def update_player(
    player_id: UUID,
    player: PlayerUpdate = Depends(),
    avatar: UploadFile | str = File(None),
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return player_crud.update_player(db, player_id, player, avatar, current_user)
