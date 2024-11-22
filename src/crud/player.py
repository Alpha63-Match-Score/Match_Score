from uuid import UUID

from src.crud.convert_db_to_response import (
    convert_db_to_player_detail_response,
    convert_db_to_player_list_response,
)
from src.models import Player
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

    if player.team_name:
        db_team = v.team_exists(db, team_name=player.team_name)

    db_player = Player(
        username=player.username,
        first_name=player.first_name,
        last_name=player.last_name,
        country=player.country,
        avatar=player.avatar,
        team_id=db_team.id if player.team_name else None,
    )

    db.add(db_player)
    db.commit()
    db.refresh(db_player)

    return convert_db_to_player_list_response(db_player)


def get_players(
    db: Session, pagination: PaginationParams, search: str | None = None
) -> list[PlayerListResponse]:

    query = db.query(Player).order_by(Player.username.asc())

    filters = []

    if search:
        filters.append(Player.username.ilike(f"%{search}%"))

    if filters:
        query = db.query(Player).filter(*filters)

    query = query.offset(pagination.offset).limit(pagination.limit)

    db_players = query.all()
    return [convert_db_to_player_list_response(db_player) for db_player in db_players]


def get_player(db: Session, player_id: UUID) -> PlayerDetailResponse:
    db_player = v.player_exists(db, player_id)

    tournament_title = None
    if db_player.team_id and db_player.team.tournament_id:
        tournament_title = db_player.team.tournament.title

    return convert_db_to_player_detail_response(db_player, tournament_title)


def update_player(
    db: Session, player_id: UUID, player: PlayerUpdate, current_user: UserResponse
) -> PlayerListResponse:
    db_player = v.player_exists(db, player_id=player_id)

    if db_player.user_id:
        v.player_update_current_user_authorization(db_player, current_user)
    else:
        v.director_or_admin(current_user)

    if player.username:
        db_player.username = player.username
    if player.first_name:
        db_player.first_name = player.first_name
    if player.last_name:
        db_player.last_name = player.last_name
    if player.country:
        db_player.country = player.country
    if player.avatar:
        db_player.avatar = player.avatar
    if player.team_name:
        team = v.team_exists(db, team_name=player.team_name)
        db_player.team_id = team.id

    db.commit()
    db.refresh(db_player)

    return convert_db_to_player_list_response(db_player)
