from datetime import datetime, timedelta, timezone
import random
from typing import Literal, Type

from src.crud import constants as c, team as crud_team
from src.crud.convert_db_to_response import convert_db_to_match_response, convert_db_to_match_list_response
from src.models import Team, Tournament
from src.models.enums import MatchFormat, Role, Stage, TournamentFormat
from src.models.match import Match
from src.schemas.schemas import (
    MatchDetailResponse,
    MatchListResponse,
    MatchUpdate,
    UserResponse,
)
from src.utils import validators as v
from src.utils.notifications import send_email_notification
from src.utils.pagination import PaginationParams

from fastapi import HTTPException
from sqlalchemy import UUID, or_
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST


def get_all_matches(
    db: Session,
    current_user: UserResponse,
    pagination: PaginationParams,
    tournament_title: str | None = None,
    stage: Stage | None = None,
    is_finished: bool | None = None,
    team_name: str | None = None,
    author: Literal["true", "false"] | None = None,
) -> list[MatchListResponse]:

    query = db.query(Match).order_by(Match.start_time.asc())

    filters = []
    if tournament_title:
        v.tournament_exists(db, tournament_title=tournament_title)
        filters.append(Match.tournament.title == tournament_title)
    if stage is not None:
        filters.append(Match.stage == stage)
    if is_finished is not None:
        filters.append(Match.is_finished == is_finished)
    if team_name:
        v.team_exists(db, team_name=team_name)
        filters.append(or_(Match.team1_id == team_name, Match.team2_id == team_name))
    if author:
        filters.append(Match.tournament.director_id == current_user.id)

    if filters:
        query = query.filter(*filters)

    query = query.offset(pagination.offset).limit(pagination.limit)

    db_matches = query.all()

    return [convert_db_to_match_list_response(db_match) for db_match in db_matches]


def get_match(db: Session, match_id: UUID) -> MatchDetailResponse:

    db_match = v.match_exists(db, match_id)

    return convert_db_to_match_response(db_match)


def generate_matches(db: Session, db_tournament: Tournament):
    matches = []
    time_format = "%B %d, %Y at %H:%M"

    # Get the team pairs and the first match datetime
    if (
        db_tournament.tournament_format == TournamentFormat.ROUND_ROBIN
        and db_tournament.current_stage == Stage.GROUP_STAGE
    ):
        team_pairs, first_match_datetime = _get_pairs_robin_round(db_tournament)
    else:
        team_pairs, first_match_datetime = _get_pairs_single_elimination(db_tournament)

    # Generate the matches and the start times
    current_time = first_match_datetime
    for i, (team1, team2) in enumerate(team_pairs):

        if current_time.hour > c.END_HOUR:
            current_time = (current_time + timedelta(days=1)).replace(hour=11, minute=0)

        match = Match(
            match_format=(
                MatchFormat.MR12
                if db_tournament.current_stage == Stage.GROUP_STAGE
                else MatchFormat.MR15
            ),
            start_time=current_time,
            stage=db_tournament.current_stage,
            team1_id=team1.id,
            team2_id=team2.id,
            tournament_id=db_tournament.id,
        )
        matches.append(match)

        for player in team1.players:
            if player.user_id is not None:
                send_email_notification(
                    email=player.user.email,
                    subject="Match Created",
                    message=f"Your match for the '{db_tournament.title}' tournament has been scheduled. You will be playing against {team2.name} on {current_time.strftime(time_format)}.",
                )

        for player in team2.players:
            if player.user_id is not None:
                send_email_notification(
                    email=player.user.email,
                    subject="Match Created",
                    message=f"Your match for the '{db_tournament.title}' tournament has been scheduled. You will be playing against {team1.name} on {current_time.strftime(time_format)}.",
                )

        current_time += timedelta(minutes=c.MATCH_DURATION_PLUS_BUFFER)

    db.bulk_save_objects(matches)


def _get_pairs_robin_round(db_tournament: Tournament) -> tuple:
    teams = db_tournament.teams
    team_pairs = []

    for i, team1 in enumerate(teams):
        for team2 in teams[i + 1 :]:
            team_pairs.append((team1, team2))

    stage_date = (
        db_tournament.start_date
        if (
            db_tournament.tournament_format == TournamentFormat.ROUND_ROBIN
            and db_tournament.current_stage == Stage.GROUP_STAGE
        )
        else db_tournament.end_date
    )
    first_match_datetime = stage_date.replace(
        hour=11, minute=0, second=0, microsecond=0
    )

    return team_pairs, first_match_datetime


def _get_pairs_single_elimination(db_tournament: Tournament) -> tuple:
    teams = db_tournament.teams
    team_pairs = []

    shuffled_teams = random.sample(teams, len(teams))
    for i in range(0, len(shuffled_teams), 2):
        team_pairs.append((shuffled_teams[i], shuffled_teams[i + 1]))

    stage_date = db_tournament.end_date - timedelta(
        days=c.STAGE_DAYS[db_tournament.current_stage]
    )
    first_match_datetime = stage_date.replace(
        hour=11, minute=0, second=0, microsecond=0
    )

    return team_pairs, first_match_datetime


def update_match(
    db: Session, match_id: UUID, match: MatchUpdate, current_user
) -> MatchDetailResponse:
    time_format = "%B %d, %Y at %H:%M"

    try:
        db.begin_nested()

        # Validating the match data
        v.director_or_admin(current_user)
        db_match = v.match_exists(db, match_id)

        if current_user.role == Role.DIRECTOR:
            v.is_author_of_tournament(db, db_match.tournament.id, current_user.id)

        v.match_is_finished(db_match)
        v.match_has_started(db_match)

        # Validating the start time
        if match.start_time:
            if (
                match.start_time < db_match.tournament.start_date
                or match.start_time > db_match.tournament.end_date
                or match.start_time < datetime.now(timezone.utc)
            ):
                raise HTTPException(
                    status_code=HTTP_400_BAD_REQUEST, detail="Invalid start time"
                )

            send_email_notification(
                email=db_match.tournament.director.email,
                subject="Match Updated",
                message=f"Match's date has been updated from {db_match.start_time.strftime(time_format)} to {match.start_time.strftime(time_format)}",
            )
        if match.team1_id:
            v.team_exists(db, match.team1_id)
            db_match.team1.tournament_id = None

        if match.team2_id:
            v.team_exists(db, match.team2_id)
            db_match.team2.tournament_id = None

        # Creating a dictionary with the updated data
        update_data = match.model_dump(exclude_unset=True)

        # Updating the data
        for key, value in update_data.items():
            setattr(db_match, key, value)

        if match.team1_id:
            db_match.team1.tournament_id = db_match.tournament_id
            for player in db_match.team1.players:
                if player.user_id is not None:
                    send_email_notification(
                        email=player.user.email,
                        subject="Match Updated",
                        message=f"Your match for the '{db_match.tournament.title}'tournament has been scheduled. You will be playing against {db_match.team2.name} on {db_match.start_time.strftime(time_format)}",
                    )

        if match.team2_id:
            db_match.team2.tournament_id = db_match.tournament_id
            for player in db_match.team2.players:
                if player.user_id is not None:
                    send_email_notification(
                        email=player.user.email,
                        subject="Match Updated",
                        message=f"Your match for the '{db_match.tournament.title}'tournament has been scheduled. You will be playing against {db_match.team1.name} on {db_match.start_time.strftime(time_format)}",
                    )

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
    current_user,
) -> MatchDetailResponse:

    try:
        db.begin_nested()

        # Validating the match data
        v.director_or_admin(current_user)
        db_match = v.match_exists(db, match_id)

        if current_user.role == Role.DIRECTOR:
            v.is_author_of_tournament(db, db_match.tournament.id, current_user.id)

        v.match_is_finished(db_match)

        v.team_has_five_players(db_match.team1)
        v.team_has_five_players(db_match.team2)

        # Creating a dictionary with the updated data
        if team_to_upvote_score == "team1":
            db_match.team1_score += 1
        else:
            db_match.team2_score += 1

        db.flush()

        # Check if the match is finished
        if db_match.match_format == MatchFormat.MR15:
            losing_team = _check_for_winner_for_mr15(db, db_match)
        elif db_match.match_format == MatchFormat.MR12:
            losing_team = _check_for_winner_for_mr12(db, db_match)

        db.flush()
        db.refresh(db_match)

        if db_match.is_finished:
            if db_match.stage == Stage.FINAL:
                _match_team_prizes(db, db_match)
            elif db_match.tournament.tournament_format != TournamentFormat.ROUND_ROBIN:
                losing_team.tournament_id = None
                db.flush()

        if all(match.is_finished for match in db_match.tournament.matches):
            if db_match.tournament.current_stage != Stage.FINISHED:
                _update_current_stage(db, db_match.tournament.id)

            if db_match.tournament.current_stage != Stage.FINISHED:
                generate_matches(db, db_match.tournament)

        db.commit()
        db.refresh(db_match)
        db.refresh(db_match.tournament)

        return convert_db_to_match_response(db_match)

    except Exception as e:
        db.rollback()
        raise e


def _update_current_stage(db: Session, tournament_id: UUID) -> None:
    db.begin_nested()

    db_tournament = v.tournament_exists(db, tournament_id)

    # If tournament is robin round, the top teams will be selected to move to the next stage
    if db_tournament.current_stage == Stage.GROUP_STAGE:
        crud_team.leave_top_teams_from_robin_round(db, db_tournament)

    db.flush()

    db_tournament.current_stage = db_tournament.current_stage.next_stage()

    db.flush()
    db.refresh(db_tournament)


def _match_team_prizes(db: Session, db_match: Type[Match]) -> None:
    for prize in db_match.tournament.prize_cuts:
        if prize.place == 1:
            prize.team_id = db_match.winner_team_id

        elif prize.place == 2:
            prize.team_id = (
                db_match.team1_id
                if db_match.team2_id == db_match.winner_team_id
                else db_match.team2_id
            )

        prize.team.tournament_id = None
        db.commit()
        db.refresh(prize)
        db.refresh(prize.team)


def _check_for_winner_for_mr15(db: Session, db_match: Match | Type[Match]) -> Team:
    if db_match.team1_score >= 15 and db_match.team2_score >= 15:
        if (
            db_match.team1_score >= 19
            and db_match.team1_score - db_match.team2_score >= 2
        ):
            _mark_match_as_finished(db, db_match, db_match.team1_id)
            return db_match.team2

        elif (
            db_match.team2_score >= 19
            and db_match.team2_score - db_match.team1_score >= 2
        ):
            _mark_match_as_finished(db, db_match, db_match.team2_id)
            return db_match.team1

    elif (
        db_match.team1_score >= 16 and db_match.team1_score - db_match.team2_score >= 2
    ):
        _mark_match_as_finished(db, db_match, db_match.team1_id)
        return db_match.team2

    elif (
        db_match.team2_score >= 16 and db_match.team2_score - db_match.team1_score >= 2
    ):
        _mark_match_as_finished(db, db_match, db_match.team2_id)
        return db_match.team1

    db.flush()
    db.refresh(db_match)


def _check_for_winner_for_mr12(db: Session, db_match: Match | Type[Match]) -> Team:
    if db_match.team1_score >= 12 and db_match.team2_score >= 12:
        if (
            db_match.team1_score >= 16
            and db_match.team1_score - db_match.team2_score >= 2
        ):
            _mark_match_as_finished(db, db_match, db_match.team1_id)
            return db_match.team2

        elif (
            db_match.team2_score >= 16
            and db_match.team2_score - db_match.team1_score >= 2
        ):
            _mark_match_as_finished(db, db_match, db_match.team2_id)
            return db_match.team1

    elif (
        db_match.team1_score >= 13 and db_match.team1_score - db_match.team2_score >= 2
    ):
        _mark_match_as_finished(db, db_match, db_match.team1_id)
        return db_match.team2

    elif (
        db_match.team2_score >= 13 and db_match.team2_score - db_match.team1_score >= 2
    ):
        _mark_match_as_finished(db, db_match, db_match.team2_id)
        return db_match.team1

    db.flush()
    db.refresh(db_match)


def _mark_match_as_finished(db: Session, db_match: Match, winner_team_id: UUID) -> None:

    db_match.is_finished = True
    db_match.winner_team_id = winner_team_id

    winner_team = (
        db_match.team1 if db_match.team1_id == winner_team_id else db_match.team2
    )
    loser_team = (
        db_match.team2 if db_match.team1_id == winner_team_id else db_match.team1
    )

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

