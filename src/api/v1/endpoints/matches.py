from fastapi import APIRouter, Depends
from sqlalchemy import UUID
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.schemas.match import MatchCreate, MatchUpdate, MatchListResponse, MatchDetailResponse

router = APIRouter()

# filter by author of match
# sort by date
# filter by tournament_id
# filter by team_id
# filter by stage
# filter by is_finished
# filter by match_format

@router.get("/", response_model=list[MatchListResponse])
def read_matches(db: Session = Depends(get_db),
                    sort: str  = 'desc',
                    team_id: UUID = None,
                    stage: str = None,
                    is_finished: bool = None,
                    match_format: str = None):
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



