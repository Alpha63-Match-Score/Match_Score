from datetime import datetime, timedelta
from typing import Type

from fastapi import HTTPException
from sqlalchemy import UUID, or_
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import random
from starlette.status import HTTP_400_BAD_REQUEST

from src.models import Tournament, Team
from src.models.enums import Stage, MatchFormat, TournamentFormat
from src.models.match import Match
from src.schemas.schemas import MatchListResponse, MatchDetailResponse, MatchCreate, MatchUpdate, MatchUpdateScore
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

    return [convert_db_to_match_list_response(db_match) for db_match in db_matches]


def get_match(
        db: Session,
        match_id: UUID
) -> MatchDetailResponse:

    v.match_exists(db, match_id)
    db_match = db.query(Match).filter(Match.id == match_id).first()

    return convert_db_to_match_response(db_match)


def generate_matches(db: Session, db_tournament
) -> None:

    if db_tournament.tournament_format == TournamentFormat.ROUND_ROBIN:
        _generate_round_robin_matches(db, db_tournament)
    else:
        _generate_single_elimination_matches(db, db_tournament)


def _generate_round_robin_matches(db: Session, db_tournament: Tournament) -> None:
    teams = db_tournament.teams
    matches = []

    for i, team1 in enumerate(teams):
        for team2 in teams[i + 1:]:
            match = Match(
                match_format=MatchFormat.MR12,
                stage=Stage.GROUP_STAGE,
                team1_id=team1.id,
                team2_id=team2.id,
                tournament_id=db_tournament.id
            )
            matches.append(match)

    match_dates = _distribute_matches_dates(db_tournament.start_date, db_tournament.end_date, len(matches))

    for match in matches:
        match.start_time = match_dates.pop(0)

    db.bulk_save_objects(matches)
    db.commit()

def _generate_single_elimination_matches(db: Session, db_tournament: Tournament) -> None:
    teams = db_tournament.teams
    shuffled_teams = random.sample(teams, len(teams))
    match_dates = _distribute_matches_dates(db_tournament.start_date, db_tournament.end_date, len(teams) // 2)

    for i in range(0, len(shuffled_teams), 2):
        db_match = Match(
            match_format = MatchFormat.MR12 if db_tournament.current_stage == Stage.GROUP_STAGE else MatchFormat.MR15,
            start_time=match_dates.pop(0),
            is_finished=False,
            stage=db_tournament.current_stage,
            team1_id=shuffled_teams[i].id,
            team2_id=shuffled_teams[i + 1].id,
            tournament_id=db_tournament.id
        )

        db.commit()
        db.refresh(db_match)


def _distribute_matches_dates(
        start_date: datetime,
        end_date: datetime,
        matches_count: int
) -> list[datetime]:

    total_days = (end_date - start_date).days

    if matches_count == 1:
        middle_date = start_date + (end_date - start_date) / 2
        return [middle_date]

    interval = total_days / (matches_count + 1)

    match_dates = []
    for i in range(matches_count):
        match_date = start_date + timedelta(days=interval * (i + 1))
        match_dates.append(match_date)

    return match_dates


def update_match(
        db: Session,
        match_id: UUID,
        match: MatchUpdate,
        current_user
) -> MatchDetailResponse:

    v.director_or_admin(current_user)

    v.match_exists(db, match_id)
    if match.start_time:
        v.validate_start_time(match.start_time)
    db_match = db.query(Match).filter(Match.id == match_id).first()

    # Creating a dictionary with the updated data
    update_data = match.model_dump(exclude_unset=True)

    # Updating the data
    for key, value in update_data.items():
        setattr(db_match, key, value)

    db.commit()
    db.refresh(db_match)

    return convert_db_to_match_response(db_match)

def update_match_score(
        db: Session,
        match_id: UUID,
        match: MatchUpdateScore,
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

    if db_match.match_format == MatchFormat.MR15:
        _check_for_winner_for_mr15(db_match)

    elif db_match.match_format == MatchFormat.MR12:
        _check_for_winner_for_mr12(db_match)

    if match.is_finished and db_match.tournament.current_stage == Stage.FINAL:
        _match_team_prizes(db, db_match)

    elif (match.is_finished
          and db_match.tournament.current_stage != Stage.FINAL
          and db_match.tournament.tournament_format != TournamentFormat.ROUND_ROBIN):

        for team in match.teams:
            if team.id != match.winner_id:
                team.tournament_id = None

                db.commit()
                db.refresh(team)

    db.commit()
    db.refresh(db_match)

    return convert_db_to_match_response(db_match)

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


def _check_for_winner_for_mr15(db_match: Match | Type[Match]) -> None:
    if db_match.team1_score >= 16 and db_match.team1_score - db_match.team2_score >= 2:
        _mark_match_as_finished(db_match, db_match.team1_id)

    elif db_match.team2_score >= 16 and db_match.team2_score - db_match.team1_score >= 2:
        _mark_match_as_finished(db_match, db_match.team2_id)

    elif db_match.team1_score >= 15 and db_match.team2_score >= 15:
        if db_match.team1_score >= 19 and db_match.team1_score - db_match.team2_score >= 2:
            _mark_match_as_finished(db_match, db_match.team1_id)

        elif db_match.team2_score >= 19 and db_match.team2_score - db_match.team1_score >= 2:
            _mark_match_as_finished(db_match, db_match.team2_id)


def _check_for_winner_for_mr12(db_match: Match | Type[Match]) -> None:
    if db_match.team1_score >= 13 and db_match.team1_score - db_match.team2_score >= 2:
        _mark_match_as_finished(db_match, db_match.team1_id)

    elif db_match.team2_score >= 13 and db_match.team2_score - db_match.team1_score >= 2:
        _mark_match_as_finished(db_match, db_match.team2_id)

    elif db_match.team1_score >= 12 and db_match.team2_score >= 12:
        if db_match.team1_score >= 16 and db_match.team1_score - db_match.team2_score >= 2:
            _mark_match_as_finished(db_match, db_match.team1_id)

        elif db_match.team2_score >= 16 and db_match.team2_score - db_match.team1_score >= 2:
            _mark_match_as_finished(db_match, db_match.team2_id)


def _mark_match_as_finished(db_match: Match, winner_team: UUID) -> None:
    db_match.is_finished = True
    db_match.winner_team_id = winner_team

    for player in db_match.team1.players:
        player.games_played += 1
        if player.team_id == winner_team:
            player.games_won += 1

    for player in db_match.team2.players:
        player.games_played += 1
        if player.team_id == winner_team:
            player.games_won += 1

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
        tournament_id=db_match.tournament_id
    )