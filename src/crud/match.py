from sqlalchemy import UUID, or_
from sqlalchemy.orm import Session

from src.models.enums import Stage
from src.models.match import Match
from src.schemas.match import MatchListResponse


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

    return [MatchListResponse(id=match.id,
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

