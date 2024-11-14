from typing import Type

from fastapi import HTTPException
from sqlalchemy import UUID, or_
from sqlalchemy.orm import Session
from src.models.team import Team
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from src.models import Tournament
from src.models.enums import Stage, Role
from src.models.match import Match
from src.schemas.match import MatchListResponse, MatchDetailResponse, MatchCreate, MatchUpdate


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
        filters.append(Match.tournament_id == tournament_id)
    if stage:
        filters.append(Match.stage == stage)
    if is_finished is not None:
        filters.append(Match.is_finished == is_finished)
    if team_id:
        filters.append(or_(Match.team1_id == team_id, Match.team2_id == team_id))

    if filters:
        query = query.filter(*filters)

    db_matches = query.all()

    return [_convert_db_to_match_list_response(db_match) for db_match in db_matches]


def get_match(
        db: Session,
        match_id: UUID
) -> MatchDetailResponse:

    db_match = db.query(Match).filter(Match.id == match_id).first()

    if not db_match:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Match not found")

    return _convert_db_to_match_response(db_match)


def create_match(
        db: Session,
        match: MatchCreate,
        current_user
) -> MatchDetailResponse:

    if current_user.role != Role.ADMIN or current_user.role != Role.DIRECTOR:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="User is not authorized to create a match")

    tournament = db.query(Tournament).filter(Tournament.id == match.tournament_id).first()
    if tournament is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Tournament not found")

    if match.team1_id == match.team2_id:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Teams should be different")

    team1 = db.query(Team).filter(Team.id == match.team1_id).first()
    if team1 is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Team 1 not found")

    team2 = db.query(Team).filter(Team.id == match.team2_id).first()
    if team2 is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Team 2 not found")

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

    if current_user.role != Role.ADMIN or current_user.role != Role.DIRECTOR:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="User is not authorized to create a match")

    db_match = db.query(Match).filter(Match.id == match_id).first()

    if not db_match:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Match not found")

    if match.stage is not None:
        db_match.stage = match.stage
    if match.start_time is not None:
        db_match.start_time = match.start_time
    if match.is_finished is not None:
        db_match.is_finished = match.is_finished
    if match.team1_score is not None:
        db_match.team1_score = match.team1_score
    if match.team2_score is not None:
        db_match.team2_score = match.team2_score

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