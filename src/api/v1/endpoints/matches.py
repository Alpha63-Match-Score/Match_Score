from fastapi import APIRouter, Depends, status
from uuid import UUID
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.crud import match
from src.models.enums import Stage
from src.schemas.match import MatchCreate, MatchUpdate, MatchListResponse, MatchDetailResponse


router = APIRouter()


@router.get("/", response_model=list[MatchListResponse])
def read_matches(
        db: Session = Depends(get_db),
        tournament_id: UUID | None = None,
        stage: Stage | None = None,
        is_finished: bool | None = None,
        team_id: UUID | None = None
):

    return match.get_all_matches(db, tournament_id, stage, is_finished, team_id)


@router.get("/{match_id}", response_model=MatchDetailResponse)
def read_match(
        match_id: UUID,
        db: Session = Depends(get_db)
):

    return match.get_match(db, match_id)


@router.post("/", response_model=MatchDetailResponse, status_code=status.HTTP_201_CREATED)
def create_match(
        match: MatchCreate,
        db: Session = Depends(get_db)
):

        return match.create_match(db, match)


@router.put("/{match_id}", response_model=MatchDetailResponse)
def update_match(match_id: UUID,
                 match: MatchUpdate,
                 db: Session = Depends(get_db)):
    pass



