from typing import Type

from fastapi import HTTPException
from sqlalchemy import UUID, or_
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from src.models.enums import Stage
from src.models.match import Match
from src.schemas.match import MatchListResponse, MatchDetailResponse, MatchCreate, MatchUpdate
from src.utils import validators as v


def get_all_matches(
        db: Session,
        tournament_id: UUID | None = None,
        stage: Stage | None = None,
        is_finished: bool | None = None,
        team_id: UUID | None = None
) -> list[MatchListResponse]:

    query = db.query(Match).order_by(Match.start_time.asc())

    filters = []
    if tournament_id:
        v.tournament_exists(db, tournament_id)
        filters.append(Match.tournament_id == tournament_id)
    if stage:
        v.stage_exists(stage)
        filters.append(Match.stage == stage)
    if is_finished is not None:
        filters.append(Match.is_finished == is_finished)
    if team_id:
        v.team_exists(db, team_id)
        filters.append(or_(Match.team1_id == team_id, Match.team2_id == team_id))

    if filters:
        query = query.filter(*filters)

    db_matches = query.all()

    return [_convert_db_to_match_list_response(db_match) for db_match in db_matches]


def get_match(
        db: Session,
        match_id: UUID
) -> MatchDetailResponse:

    v.match_exists(db, match_id)
    db_match = db.query(Match).filter(Match.id == match_id).first()

    return _convert_db_to_match_response(db_match)


def create_match(
        db: Session,
        match: MatchCreate,
        current_user
) -> MatchDetailResponse:

    v.director_or_admin(current_user)
    v.tournament_exists(db, match.tournament_id)

    if match.team1_id == match.team2_id:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Teams should be different")

    v.team_exists(db, match.team1_id)
    v.team_exists(db, match.team2_id)

    db_match = Match(**match.model_dump())

    db.add(db_match)
    db.commit()
    db.refresh(db_match)

    return _convert_db_to_match_response(db_match)


def update_match(
        db: Session,
        match_id: UUID,
        match: MatchUpdate,
        current_user
) -> MatchDetailResponse:

    v.director_or_admin(current_user)

    v.match_exists(db, match_id)
    db_match = db.query(Match).filter(Match.id == match_id).first()

    # Creating a dictionary with the updated data
    update_data = match.model_dump(exclude_unset=True)

    # Updating the data
    for key, value in update_data.items():
        setattr(db_match, key, value)

    db.commit()
    db.refresh(db_match)

    return _convert_db_to_match_response(db_match)


def _convert_db_to_match_response(db_match: Match | Type[Match]) -> MatchDetailResponse:
    return MatchDetailResponse(
        id=db_match.id,
        match_format=db_match.match_format,
        start_time=db_match.start_time,
        is_finished=db_match.is_finished,
        stage=db_match.stage,
        team1_id=db_match.team1_id,
        team2_id=db_match.team2_id,
        team1_score=db_match.team1_score,
        team2_score=db_match.team2_score,
        tournament_id=db_match.tournament_id,
        team1_name=db_match.team1.name,
        team2_name=db_match.team2.name,
        team1_logo=db_match.team1.logo,
        team2_logo=db_match.team2.logo,
        tournament_title=db_match.tournament.title
    )


def _convert_db_to_match_list_response(db_match: Match | Type[Match]) -> MatchListResponse:
    return MatchListResponse(
        id=db_match.id,
        match_format=db_match.match_format,
        start_time=db_match.start_time,
        is_finished=db_match.is_finished,
        stage=db_match.stage,
        team1_id=db_match.team1_id,
        team2_id=db_match.team2_id,
        team1_score=db_match.team1_score,
        team2_score=db_match.team2_score,
        tournament_id=db_match.tournament_id
    )