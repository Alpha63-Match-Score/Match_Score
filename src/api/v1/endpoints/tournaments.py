from fastapi import APIRouter, Depends
from sqlalchemy import UUID
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.schemas.tournament import TournamentListResponse, TournamentDetailResponse, TournamentCreate, TournamentUpdate

router = APIRouter()

@router.get("/", response_model=list[TournamentListResponse])
def read_tournaments(db: Session = Depends(get_db)):
    pass

@router.get("/{tournament_id}", response_model=TournamentDetailResponse)
def read_tournament(tournament_id: UUID,
                    db: Session = Depends(get_db)):
    pass

@router.post("/", response_model=TournamentDetailResponse)
def create_tournament(tournament: TournamentCreate,
                      db: Session = Depends(get_db)):
    pass

@router.put("/{tournament_id}", response_model=TournamentDetailResponse)
def update_tournament(tournament_id: UUID,
                      tournament: TournamentUpdate,
                      db: Session = Depends(get_db)):
    pass

