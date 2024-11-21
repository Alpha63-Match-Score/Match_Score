from typing import Literal
from uuid import UUID

from src.api.deps import get_current_user, get_db
from src.crud import tournament as tournament_crud
from src.schemas.schemas import (
    TournamentCreate,
    TournamentDetailResponse,
    TournamentListResponse,
    TournamentUpdate,
    UserResponse,
)
from src.utils.pagination import PaginationParams, get_pagination

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


# filter by author of tournament
@router.get("/", response_model=list[TournamentListResponse])
def read_tournaments(
    pagination: PaginationParams = Depends(get_pagination),
    period: Literal["past", "present", "future"] | None = None,
    status: Literal["active", "finished"] | None = None,
    search: str | None = None,
    author: Literal["true", "false"] | None = None,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return tournament_crud.get_tournaments(
        db, current_user, pagination, period, status, search, author
    )


@router.get("/{tournament_id}", response_model=TournamentDetailResponse)
def read_tournament(tournament_id: UUID, db: Session = Depends(get_db)):
    return tournament_crud.get_tournament(db, tournament_id)


@router.post("/", response_model=TournamentDetailResponse, status_code=201)
def create_tournament(
    tournament: TournamentCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return tournament_crud.create_tournament(db, tournament, current_user)


@router.put("/{tournament_id}", response_model=TournamentDetailResponse)
def update_tournament(
    tournament_id: UUID,
    tournament: TournamentUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user),
):
    return tournament_crud.update_tournament(
        db, tournament_id, tournament, current_user
    )


# @router.put("/{tournament_id}/stages", response_model=TournamentDetailResponse)
# def update_tournament(tournament_id: UUID,
#                       db: Session = Depends(get_db),
#                       current_user: UserResponse = Depends(get_current_user)
# ):
#
#     return tournament_crud.update_tournament_stage(db, tournament_id, current_user)
