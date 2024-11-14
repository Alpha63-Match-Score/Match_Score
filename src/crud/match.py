from sqlalchemy import UUID, or_
from sqlalchemy.orm import Session

from src.models.enums import Stage
from src.models.match import Match
from src.schemas.match import MatchListResponse, MatchDetailResponse


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

    return [MatchListResponse(
        id=match.id,
        match_format=match.match_format,
        start_time=match.start_time,
        is_finished=match.is_finished,
        stage=match.stage,
        team1_id=match.team1_id,
        team2_id=match.team2_id,
        team1_score=match.team1_score,
        team2_score=match.team2_score,
        tournament_id=match.tournament_id
    )
        for match in db_matches
    ]

def get_match(
        db: Session,
        match_id: UUID
) -> MatchDetailResponse:

    db_match = db.query(Match).filter(Match.id == match_id).first()

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

