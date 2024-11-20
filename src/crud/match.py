from datetime import timedelta
from fastapi import HTTPException
import random
from typing import Type, Literal

from sqlalchemy import UUID, or_
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from src.models import Tournament
from src.models.match import Match
from src.crud import team as crud_team
from src.models.enums import Stage, MatchFormat, TournamentFormat

from src.schemas.schemas import (MatchListResponse,
                                 MatchDetailResponse,
                                 MatchUpdate)

from src.crud import constants as c
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
    if stage is not None:
        filters.append(Match.stage == stage)
    if is_finished is not None:
        filters.append(Match.is_finished == is_finished)
    if team_id:
        v.team_exists(db, team_id)
        filters.append(or_(Match.team1_id == team_id, Match.team2_id == team_id))

    if filters:
        query = query.filter(*filters)

    db_matches = query.all()

    return [convert_db_to_match_list_response(db_match) for db_match in db_matches]


def get_match(
        db: Session,
        match_id: UUID
) -> MatchDetailResponse:

    db_match = v.match_exists(db, match_id)

    return convert_db_to_match_response(db_match)


def generate_matches(
        db: Session,
        db_tournament: Tournament
):
    matches = []

    # Get the team pairs and the first match datetime
    if db_tournament.tournament_format == TournamentFormat.ROUND_ROBIN:
        team_pairs, first_match_datetime = _get_pairs_robin_round(db_tournament)
    else:
        team_pairs, first_match_datetime = _get_pairs_single_elimination(db_tournament)

    # Generate the matches and the start times
    current_time = first_match_datetime
    for i, (team1, team2) in enumerate(team_pairs):

        if current_time.hour > c.END_HOUR:
            current_time = (current_time + timedelta(days=1)).replace(hour=11, minute=0)

        match = Match(
            match_format=MatchFormat.MR12 if db_tournament.current_stage == Stage.GROUP_STAGE else MatchFormat.MR15,
            start_time=current_time,
            stage=db_tournament.current_stage,
            team1_id=team1.id,
            team2_id=team2.id,
            tournament_id=db_tournament.id
        )
        matches.append(match)

        current_time += timedelta(minutes=c.MATCH_DURATION_PLUS_BUFFER)

    db.bulk_save_objects(matches)


def _get_pairs_robin_round(db_tournament: Tournament) -> tuple:
    teams = db_tournament.teams
    team_pairs = []

    for i, team1 in enumerate(teams):
        for team2 in teams[i + 1:]:
            team_pairs.append((team1, team2))


    stage_date = db_tournament.start_date if db_tournament.tournament_format == TournamentFormat.ROUND_ROBIN \
        else db_tournament.end_date
    first_match_datetime = stage_date.replace(hour=11, minute=0, second=0, microsecond=0)

    return team_pairs, first_match_datetime

def _get_pairs_single_elimination(db_tournament: Tournament) -> tuple:
    teams = db_tournament.teams
    team_pairs = []

    shuffled_teams = random.sample(teams, len(teams))
    for i in range(0, len(shuffled_teams), 2):
        team_pairs.append((shuffled_teams[i], shuffled_teams[i + 1]))

    stage_date = db_tournament.end_date - timedelta(days=c.STAGE_DAYS[db_tournament.current_stage])
    first_match_datetime = stage_date.replace(hour=11, minute=0, second=0, microsecond=0)

    return team_pairs, first_match_datetime


def update_match(
        db: Session,
        match_id: UUID,
        match: MatchUpdate,
        current_user
) -> MatchDetailResponse:

    try:
        db.begin_nested()

        # Validating the match data
        v.director_or_admin(current_user)
        v.is_author_of_tournament(db, match.tournament_id, current_user.id)
        db_match = v.match_exists(db, match_id)

        if db_match.is_finished:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Match is already finished")

        if match.start_time:
            if (match.start_time < db_match.tournament.start_date
                    or match.start_time > db_match.tournament.end_date):
                raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Invalid start time")

        # Creating a dictionary with the updated data
        update_data = match.model_dump(exclude_unset=True)

        # Updating the data
        for key, value in update_data.items():
            setattr(db_match, key, value)

        db.commit()
        db.refresh(db_match)

        return convert_db_to_match_response(db_match)

    except Exception as e:
        db.rollback()
        raise e


def update_match_score(
        db: Session,
        match_id: UUID,
        team_to_upvote_score: Literal["team1", "team2"],
        current_user
) -> MatchDetailResponse:

    try:
        db.begin_nested()

        # Validating the match data
        v.director_or_admin(current_user)
        db_match = v.match_exists(db, match_id)
        v.is_author_of_tournament(db, db_match.tournament.id, current_user.id)

        if db_match.is_finished:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Match is already finished")

        # Creating a dictionary with the updated data
        if team_to_upvote_score == "team1":
            db_match.team1_score += 1
        else:
            db_match.team2_score += 1

        db.flush()

        # Check if the match is finished
        if db_match.match_format == MatchFormat.MR15:
            _check_for_winner_for_mr15(db, db_match)
        elif db_match.match_format == MatchFormat.MR12:
            _check_for_winner_for_mr12(db, db_match)

        db.flush()
        db.refresh(db_match)

        # If the tournament is finished, update the team prizes
        if db_match.is_finished and db_match.stage == Stage.FINAL:
            _match_team_prizes(db, db_match)

        if (not db_match.is_finished
              and db_match.tournament.current_stage != Stage.FINAL
              and db_match.tournament.tournament_format != TournamentFormat.ROUND_ROBIN):

            losing_team = next(
                team for team in [db_match.team1, db_match.team2]
                if team.id != db_match.winner_team_id)
            losing_team.tournament_id = None
            db.flush()

        if all(match.is_finished for match in db_match.tournament.matches):
            _update_current_stage(db, db_match.tournament.id)

        db.commit()
        db.refresh(db_match)
        db.refresh(db_match.tournament)

        return convert_db_to_match_response(db_match)

    except Exception as e:
        db.rollback()
        raise e


def _update_current_stage(
    db: Session,
    tournament_id: UUID
) -> None:
    db.begin_nested()

    db_tournament = v.tournament_exists(db, tournament_id)

    # If tournament is robin round, the top teams will be selected to move to the next stage
    if db_tournament.current_stage == Stage.GROUP_STAGE:
        crud_team.leave_top_teams_from_robin_round(db_tournament)

    db_tournament.current_stage = db_tournament.current_stage.next_stage()
    db.flush()
    db.refresh(db_tournament)


def _match_team_prizes(db: Session, db_match: Type[Match]) -> None:
    for prize in db_match.tournament.prize_cuts:
        if prize.place == 1:
            prize.team_id = db_match.winner_team_id

        elif prize.place == 2:
            prize.team_id = db_match.team1_id if db_match.team2_id == db_match.winner_team_id \
                else db_match.team2_id

        prize.team.tournament_id = None
        db.commit()
        db.refresh(prize)
        db.refresh(prize.team)


def _check_for_winner_for_mr15(db: Session, db_match: Match | Type[Match]) -> None:
    if db_match.team1_score >= 15 and db_match.team2_score >= 15:
        if db_match.team1_score >= 19 and db_match.team1_score - db_match.team2_score >= 2:
            _mark_match_as_finished(db, db_match, db_match.team1_id)

        elif db_match.team2_score >= 19 and db_match.team2_score - db_match.team1_score >= 2:
            _mark_match_as_finished(db, db_match, db_match.team2_id)

    elif db_match.team1_score >= 16 and db_match.team1_score - db_match.team2_score >= 2:
        _mark_match_as_finished(db, db_match, db_match.team1_id)

    elif db_match.team2_score >= 16 and db_match.team2_score - db_match.team1_score >= 2:
        _mark_match_as_finished(db, db_match, db_match.team2_id)

    db.flush()
    db.refresh(db_match)


def _check_for_winner_for_mr12(db: Session, db_match: Match | Type[Match]) -> None:
    if db_match.team1_score >= 12 and db_match.team2_score >= 12:
        if db_match.team1_score >= 16 and db_match.team1_score - db_match.team2_score >= 2:
            _mark_match_as_finished(db, db_match, db_match.team1_id)

        elif db_match.team2_score >= 16 and db_match.team2_score - db_match.team1_score >= 2:
            _mark_match_as_finished(db, db_match, db_match.team2_id)

    elif db_match.team1_score >= 13 and db_match.team1_score - db_match.team2_score >= 2:
        _mark_match_as_finished(db, db_match, db_match.team1_id)

    elif db_match.team2_score >= 13 and db_match.team2_score - db_match.team1_score >= 2:
        _mark_match_as_finished(db, db_match, db_match.team2_id)

    db.flush()
    db.refresh(db_match)


def _mark_match_as_finished(
        db: Session,
        db_match: Match,
        winner_team_id: UUID
) -> None:

    db_match.is_finished = True
    db_match.winner_team_id = winner_team_id

    winner_team = db_match.team1 if db_match.team1_id == winner_team_id else db_match.team2
    loser_team = db_match.team2 if db_match.team1_id == winner_team_id else db_match.team1

    winner_team.played_games += 1
    winner_team.won_games += 1
    loser_team.played_games += 1


    for player in winner_team.players:
        player.played_games += 1
        player.won_games += 1

    for player in loser_team.players:
        player.played_games += 1

    db.flush()
    db.refresh(db_match)


def convert_db_to_match_response(db_match: Match | Type[Match]) -> MatchDetailResponse:
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
        winner_id=db_match.winner_team_id,
        tournament_id=db_match.tournament_id,
        team1_name=db_match.team1.name,
        team2_name=db_match.team2.name,
        team1_logo=db_match.team1.logo,
        team2_logo=db_match.team2.logo,
        tournament_title=db_match.tournament.title
    )


def convert_db_to_match_list_response(db_match: Match | Type[Match]) -> MatchListResponse:
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
        winner_id=db_match.winner_team_id,
        tournament_id=db_match.tournament_id
    )