from fastapi import APIRouter, Depends
from sqlalchemy import UUID
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.schemas.match import MatchCreate, MatchUpdate, MatchListResponse, MatchDetailResponse

router = APIRouter()

@router.get("/", response_model=list[MatchListResponse])
def read_matches(db: Session = Depends(get_db)):
    pass

@router.get("/{match_id}", response_model=MatchDetailResponse)
def read_match(match_id: UUID,
               db: Session = Depends(get_db)):
    pass

@router.post("/", response_model=MatchDetailResponse)
def create_match(match: MatchCreate,
                 db: Session = Depends(get_db)):
    pass

@router.put("/{match_id}", response_model=MatchDetailResponse)
def update_match(match_id: UUID,
                 match: MatchUpdate,
                 db: Session = Depends(get_db)):
    pass



