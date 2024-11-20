import math
from datetime import datetime, timedelta
from typing import Literal, Type
from uuid import UUID

from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from src.crud import match as crud_match
from src.crud import prize_cut as crud_prize_cut
from src.crud import team as crud_team

from src.models import Tournament
from src.models.enums import Stage, TournamentFormat

from src.schemas.schemas import (TournamentListResponse,
                                 TournamentDetailResponse,
                                 TournamentCreate,
                                 UserResponse,
                                 TournamentUpdate)

from src.crud import constants as c
from src.utils.pagination import PaginationParams
from src.utils import validators as v


def get_tournaments(
    db: Session,
    pagination: PaginationParams,
    period: Literal['past', 'present', 'future'] | None = None,
    search: str | None = None,
    director_id: UUID | None = None,
) -> list[TournamentListResponse]:

    query = db.query(Tournament).order_by(Tournament.start_date.asc())

    filters = []

    if period:
        if period == 'past':
            filters.append(or_(
                Tournament.end_date < datetime.now(),
                Tournament.current_stage == Stage.FINISHED
            ))
        elif period == 'present':
            filters.append(
                and_(Tournament.start_date <= datetime.now(),
                     Tournament.end_date >= datetime.now(),
                     Tournament.current_stage != Stage.FINISHED))
        elif period == 'future':
            filters.append(
                and_(Tournament.start_date > datetime.now(),
                     Tournament.current_stage != Stage.FINISHED))

    if search is not None:
        filters.append(Tournament.title.ilike(f"%{search}%"))

    if director_id:
        v.user_exists(db, director_id)
        filters.append(Tournament.director_id == director_id)

    if filters:
        query = query.filter(*filters)

    query = query.offset(pagination.offset).limit(pagination.limit)

    db_tournaments = query.all()

    return [convert_db_to_tournament_list_response(db_tournament) for db_tournament in db_tournaments]


def get_tournament(
    db: Session,
    tournament_id: UUID
) -> TournamentListResponse:

    db_tournament = v.tournament_exists(db, tournament_id)

    participants = []
    for db_match in db_tournament.matches:
        if db_match.team1_id not in participants:
            participants.append(db_match.team1)
        if db_match.team2_id not in participants:
            participants.append(db_match.team2)

    return convert_db_to_tournament_response(db_tournament)


def create_tournament(
    db: Session,
    tournament: TournamentCreate,
    current_user: UserResponse
) -> TournamentDetailResponse:

    try:
        # Creating a new tournament
        db.begin_nested()

        # Validating the tournament data
        v.unique_teams_in_tournament(tournament.team_names)
        v.tournament_title_unique(db, tournament.title)
        v.director_or_admin(current_user)
        v.validate_start_date(tournament.start_date)

        # get current stage for tournament
        total_teams = len(tournament.team_names)
        current_stage = _get_tournament_current_stage(tournament.tournament_format.value, total_teams)

        # calculating the end date
        end_date = _calculate_tournament_end_date(
            tournament.start_date,
            tournament.tournament_format,
            current_stage,
            total_teams)

        # Creating the tournament
        db_tournament = Tournament(
            title=tournament.title,
            tournament_format=TournamentFormat(tournament.tournament_format),
            start_date=tournament.start_date,
            end_date=end_date,
            prize_pool=tournament.prize_pool,
            current_stage=current_stage,
            director_id=current_user.id
        )

        db.add(db_tournament)
        db.flush()

        crud_prize_cut.create_prize_cuts_for_tournament(db, db_tournament)
        crud_team.create_teams_lst_for_tournament(db, tournament.team_names, db_tournament.id)

        db.flush()

        crud_match.generate_matches(db, db_tournament)
        tournament = convert_db_to_tournament_response(db_tournament)
        db.commit()

        return tournament

    except Exception as e:
        # Ensure no changes are made to the database
        db.rollback()
        raise e


def _get_tournament_current_stage(
        tournament_format: str,
        number_of_teams: int
) -> Stage:

    if tournament_format == TournamentFormat.SINGLE_ELIMINATION:
        if number_of_teams not in c.SINGLE_ELIMINATION_TEAMS:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Invalid number of teams for single elimination - must be 4, 8 or 16")

        if number_of_teams == 4:
            return Stage.SEMI_FINAL
        elif number_of_teams == 8:
            return Stage.QUARTER_FINAL
        else:
            return Stage.ROUND_OF_16

    elif tournament_format == TournamentFormat.ROUND_ROBIN:
        if number_of_teams not in c.ROUND_ROBIN_TEAMS:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Invalid number of teams for round robin - must be 4 or 5")
        return Stage.GROUP_STAGE

    elif tournament_format == TournamentFormat.ONE_OFF_MATCH:
        if number_of_teams not in c.ONE_OFF_MATCH_TEAMS:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Invalid number of teams for one off match - must be 2")
        return Stage.FINAL


def _calculate_tournament_end_date(
        start_date: datetime,
        tournament_format: TournamentFormat,
        current_stage: Stage,
        total_teams: int
) -> datetime:

    if tournament_format == TournamentFormat.ROUND_ROBIN:
        total_matches = total_teams * (total_teams - 1) // 2
        required_days = math.ceil((total_matches - 1) / c.MAX_MATCHES_PER_DAY) + 1
    else:
        required_days = c.STAGE_DAYS[current_stage]

    return start_date + timedelta(days=required_days)


def update_tournament(
    db: Session,
    tournament_id: UUID,
    tournament: TournamentUpdate,
    current_user: UserResponse
) -> TournamentDetailResponse:

    try:
        db.begin_nested()

        # Validating the tournament data
        v.director_or_admin(current_user)
        v.is_author_of_tournament(db, current_user.id, tournament_id)
        db_tournament = v.tournament_exists(db, tournament_id)
        v.tournament_is_finished(db_tournament)

        if current_user.role != 'admin':
            v.tournament_has_started(db_tournament)

        v.director_or_admin(current_user)
        v.is_author_of_tournament(db, current_user.id, tournament_id)


        # Creating a dictionary with the updated data
        update_data = tournament.model_dump(exclude_unset=True)

        if db_tournament.start_date >= db_tournament.end_date:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Start date must be before end date")

        # Updating the data
        for key, value in update_data.items():
            setattr(db_tournament, key, value)

        db.commit()
        db.refresh(db_tournament)

        return convert_db_to_tournament_response(db_tournament)

    except Exception as e:
        db.rollback()
        raise e


def convert_db_to_tournament_list_response(
        db_tournament: Tournament | Type[Tournament],
) -> TournamentListResponse:

    return TournamentListResponse(
        id=db_tournament.id,
        title=db_tournament.title,
        tournament_format=db_tournament.tournament_format,
        start_date=db_tournament.start_date,
        end_date=db_tournament.end_date,
        current_stage=db_tournament.current_stage,
        number_of_teams=len(db_tournament.teams),
    )


def convert_db_to_tournament_response(
        db_tournament: Tournament | Type[Tournament]
) -> TournamentDetailResponse:

    return TournamentDetailResponse(
        id=db_tournament.id,
        title=db_tournament.title,
        tournament_format=db_tournament.tournament_format,
        start_date=db_tournament.start_date,
        end_date=db_tournament.end_date,
        current_stage=db_tournament.current_stage,
        number_of_teams=len(db_tournament.teams),
        matches_of_current_stage=[crud_match.convert_db_to_match_list_response(db_match)
                 for db_match in db_tournament.matches
                 if not db_match.is_finished],
        teams=[crud_team.convert_db_to_team_list_response(db_team) for db_team in db_tournament.teams],
        prizes=[crud_prize_cut.convert_db_to_prize_cut_response(db_prize) for db_prize in db_tournament.prize_cuts]
    )