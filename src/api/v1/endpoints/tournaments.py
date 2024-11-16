from typing import Literal

from fastapi import APIRouter, Depends
from uuid import UUID
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.schemas.schemas import TournamentListResponse, TournamentDetailResponse, TournamentCreate, TournamentUpdate
from src.utils.pagination import PaginationParams, get_pagination
from src.crud import tournament as tournament_crud

router = APIRouter()

# filter by author of tournament
@router.get("/", response_model=list[TournamentListResponse])
def read_tournaments(db: Session = Depends(get_db),
                    pagination: PaginationParams = Depends(get_pagination),
                     period: Literal['past', 'present', 'future'] | None= None,
                     search: str | None = None,
                     director_id: UUID | None = None):

    return tournament_crud.get_tournaments(db, pagination, period, search, director_id)


@router.get("/{tournament_id}", response_model=TournamentDetailResponse)
def read_tournament(tournament_id: UUID,
                    db: Session = Depends(get_db)):

    return tournament_crud.get_tournament(db, tournament_id)

@router.post("/", response_model=TournamentDetailResponse)
def create_tournament(tournament: TournamentCreate,
                      db: Session = Depends(get_db)):
    pass

@router.put("/{tournament_id}", response_model=TournamentDetailResponse)
def update_tournament(tournament_id: UUID,
                      tournament: TournamentUpdate,
                      db: Session = Depends(get_db)):
    pass

