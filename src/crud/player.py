from typing import Type
from uuid import UUID

from src.crud.tournament import convert_db_to_tournament_list_response
from src.models import Player, Team, Tournament
from src.schemas.schemas import (
    PlayerCreate,
    PlayerDetailResponse,
    PlayerListResponse,
    PlayerUpdate,
    UserResponse,
)
from src.utils import validators as v
from src.utils.pagination import PaginationParams

from sqlalchemy.orm import Session


def create_player(
    db: Session, player: PlayerCreate, current_user: UserResponse
) -> PlayerListResponse:
    v.player_username_unique(db, username=player.username)
    v.director_or_admin(current_user)

    db_player = Player(
        username=player.username,
        first_name=player.first_name,
        last_name=player.last_name,
        country=player.country,
        avatar=player.avatar,
    )

    db.add(db_player)
    db.commit()
    db.refresh(db_player)

    return convert_db_to_player_list_response(db_player)


def get_players(
    db: Session, pagination: PaginationParams, search: str | None = None
) -> PlayerListResponse:

    query = db.query(Player).order_by(Player.username.asc())

    filters = []

    if search:
        filters.append(Player.username.ilike(f"%{search}%"))

    if filters:
        query = db.query(Player).filter(*filters)

    query = query.offset(pagination.offset).limit(pagination.limit)

    db_players = query.all()
    return [convert_db_to_player_list_response(db_player) for db_player in db_players]


def convert_db_to_player_list_response(db_player: Type[Player]) -> PlayerListResponse:
    return PlayerListResponse(
        id=db_player.id,
        username=db_player.username,
        first_name=db_player.first_name,
        last_name=db_player.last_name,
        country=db_player.country,
        avatar=db_player.avatar,
        team_id=db_player.team_id,
        user_id=db_player.user_id,
    )


def get_player(db: Session, player_id: UUID) -> PlayerDetailResponse:
    db_player = v.player_exists(db, player_id)
    db_tournaments = (
        db.query(Tournament)
        .join(Team)
        .join(Player)
        .filter(Player.id == player_id)
        .all()
    )
    return convert_db_to_player_detail_response(db_player, db_tournaments)


def convert_db_to_player_detail_response(
    db_player: Type[Player], db_tournaments: list[Type[Tournament]]
) -> PlayerDetailResponse:
    return PlayerDetailResponse(
        id=db_player.id,
        username=db_player.username,
        first_name=db_player.first_name,
        last_name=db_player.last_name,
        country=db_player.country,
        avatar=db_player.avatar,
        team_id=db_player.team_id,
        user_id=db_player.user_id,
        tournaments=[
            convert_db_to_tournament_list_response(db_tournament)
            for db_tournament in db_tournaments
        ],
    )


def update_player(
    db: Session, player_id: UUID, player: PlayerUpdate, current_user: UserResponse
) -> PlayerListResponse:
    db_player = v.player_exists(db, player_id=player_id)
    v.director_or_admin(current_user)

    db_player.username = (player.username,)
    db_player.first_name = (player.first_name,)
    db_player.last_name = (player.last_name,)
    db_player.country = (player.country,)
    db_player.avatar = (player.avatar,)
    db_player.team_id = (player.team_id,)
    db_player.user_id = player.user_id

    v.user_exists(db, user_id=player.user_id)
    v.team_exists(db, team_id=player.team_id)

    db.commit()
    db.refresh(db_player)

    return convert_db_to_player_list_response(db_player)
