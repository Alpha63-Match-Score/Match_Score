from datetime import datetime
from typing import Literal, Type
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST

from src.crud.match import convert_db_to_match_list_response, generate_matches
from src.crud.prize_cut import convert_db_to_prize_cut_response, create_prize_cuts_for_tournament
from src.models import Tournament, Team, User
from src.models.enums import Stage, TournamentFormat
from src.schemas.schemas import TournamentListResponse, TournamentDetailResponse, TeamListResponse, TournamentCreate, \
    UserResponse, TournamentUpdate
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
            filters.append(Tournament.end_date < datetime.now())
        elif period == 'present':
            filters.append(
                and_(Tournament.start_date <= datetime.now(),
                     Tournament.end_date >= datetime.now()))
        elif period == 'future':
            filters.append(Tournament.start_date > datetime.now())

    if search:
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

    v.tournament_exists(db, tournament_id)
    db_tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()

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

    current_stage = v.tournament_format_number_of_teams(tournament.tournament_format.value, len(tournament.team_names))
    v.tournament_title_unique(db, tournament.title)
    v.user_exists(db, current_user.id)
    v.director_or_admin(current_user)
    v.validate_start_vs_end_date(tournament.start_date, tournament.end_date)

    db_tournament = Tournament(
        title=tournament.title,
        tournament_format=TournamentFormat(tournament.tournament_format),
        start_date=tournament.start_date,
        end_date=tournament.end_date,
        prize_pool=tournament.prize_pool,
        current_stage=current_stage,
        director_id=current_user.id
    )

    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)

    create_prize_cuts_for_tournament(db, db_tournament)
    create_teams_lst_for_tournament(db, tournament.team_names, db_tournament.id)
    generate_matches(db, db_tournament)

    return convert_db_to_tournament_response(db_tournament)


# TODO
def create_teams_lst_for_tournament(
        db: Session,
        team_names: list[str],
        tournament_id: UUID
) -> None:

    teams = []
    for name in team_names:
        v.team_exists_by_name(db, name)
        db_team = db.query(Team).filter(Team.name == name).first()

        if db_team.tournament_id is not None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Team already participates in another tournament")

        if len(db_team.players) < 5:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Team must have at least 5 players")

        teams.append(db_team)

    for db_team in teams:
        db_team.tournament_id = tournament_id

    db.commit()

def update_tournament(
    db: Session,
    tournament_id: UUID,
    tournament: TournamentUpdate,
    current_user: UserResponse
) -> TournamentDetailResponse:

    v.director_or_admin(current_user)

    v.tournament_exists(db, tournament_id)
    db_tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()

    if tournament.start_date:
        v.validate_start_vs_end_date(tournament.start_date, db_tournament.end_date)
    elif tournament.end_date:
        v.validate_start_vs_end_date(db_tournament.start_date, tournament.end_date)
    elif tournament.start_date and tournament.end_date:
        v.validate_start_vs_end_date(tournament.start_date, tournament.end_date)

    # Creating a dictionary with the updated data
    update_data = tournament.model_dump(exclude_unset=True)

    # Updating the data
    for key, value in update_data.items():
        setattr(db_tournament, key, value)

    db.commit()
    db.refresh(db_tournament)

    return convert_db_to_tournament_response(db_tournament)

def update_tournament_stage(
    db: Session,
    tournament_id: UUID,
    current_user: UserResponse
) -> TournamentDetailResponse:

    v.director_or_admin(current_user)
    v.is_author_of_tournament(db, tournament_id, current_user.id)

    v.tournament_exists(db, tournament_id)
    db_tournament = db.query(Tournament).filter(Tournament.id == tournament_id).first()

    for match in db_tournament.matches:
        if not match.is_finished:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="All matches must be finished before moving to the next stage")

    if db_tournament.current_stage == Stage.GROUP_STAGE:
        leave_top_teams_from_robin_round(db, db_tournament)

    db_tournament.current_stage = db_tournament.current_stage.next_stage()

    db.commit()
    db.refresh(db_tournament)
    generate_matches(db, db_tournament)

    return convert_db_to_tournament_response(db_tournament)

# TODO
def leave_top_teams_from_robin_round(
        db: Session,
        db_tournament: Type[Tournament],
) -> None:

    team_stats = {}
    for match in db_tournament.matches:
            if match.winner_team_id not in team_stats:
                team_stats[match.winner_team] = 0
            team_stats[match.winner_team] += 1

    top_scores = sorted(team_stats.values(), reverse=True)[:2]

    best_teams = []
    for team, score in team_stats.items():
        if score in top_scores:
            best_teams.append(team)
        else:
            team.tournament_id = None

    db.commit()


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
        number_of_participants=len(db_tournament.teams),
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
        matches=[convert_db_to_match_list_response(db_match) for db_match in db_tournament.matches],
        teams=[convert_db_to_team_list_response(db_team) for db_team in db_tournament.teams],
        prizes=[convert_db_to_prize_cut_response(db_prize) for db_prize in db_tournament.prize_cuts]
    )

# TODO
def convert_db_to_team_list_response(
        db_team: Type[Team]
) -> TeamListResponse:

        return TeamListResponse(
            id=db_team.id,
            name=db_team.name,
            logo=db_team.logo,
        )