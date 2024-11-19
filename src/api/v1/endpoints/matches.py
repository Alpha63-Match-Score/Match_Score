from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.deps import get_db, get_current_user
from src.crud import match as match_crud
from src.models.enums import Stage
from src.schemas.schemas import MatchUpdate, MatchListResponse, MatchDetailResponse

router = APIRouter()


@router.get("/", response_model=list[MatchListResponse])
def read_matches(
        db: Session = Depends(get_db),
        tournament_id: UUID | None = None,
        stage: Stage | None = None,
        is_finished: bool | None = None,
        team_id: UUID | None = None
):

    return match_crud.get_all_matches(db, tournament_id, stage, is_finished, team_id)


@router.get("/{match_id}", response_model=MatchDetailResponse)
def read_match(
        match_id: UUID,
        db: Session = Depends(get_db)
):

    return match_crud.get_match(db, match_id)


# @router.post("/", response_model=MatchDetailResponse, status_code=status.HTTP_201_CREATED)
# def create_match(
#         match: MatchCreate,
#         db: Session = Depends(get_db),
#         current_user = Depends(get_current_user)
# ):
#
#         return match_crud.create_match(db, match, current_user)


@router.put("/{match_id}", response_model=MatchDetailResponse)
def update_match(
        match_id: UUID,
        match: MatchUpdate,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):

    return match_crud.update_match(db, match_id, match, current_user)

@router.put("/{match_id}/team-scores", response_model=MatchDetailResponse)
def update_match_score(
        match_id: UUID,
        team_to_upvote_score: Literal["team1", "team2"],
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):

    return match_crud.update_match_score(db, match_id, team_to_upvote_score, current_user)