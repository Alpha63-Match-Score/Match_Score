from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.orm import Session
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
from src.utils.s3 import S3Service, s3_service


def create_player(
    db: Session,
    player: PlayerCreate,
    avatar: UploadFile | None,
    current_user: UserResponse
) -> PlayerListResponse:

    v.player_username_unique(db, username=player.username)
    v.director_or_admin(current_user)

    if player.team_name:
        db_team = v.team_exists(db, team_name=player.team_name)

    avatar_url = None
    if avatar:
        avatar_url = s3_service.upload_file(avatar, "players")

    db_player = Player(
        username=player.username,
        first_name=player.first_name,
        last_name=player.last_name,
        country=player.country,
        avatar=avatar_url,
        team_id=db_team.id if player.team_name else None,
    )

    db.add(db_player)
    db.commit()
    db.refresh(db_player)

    return convert_db_to_player_list_response(db_player)


def get_players(
    db: Session,
    pagination: PaginationParams,
    search_by_player: str | None = None,
    search_by_team: str | None = None,
    sort_by: str = "asc",
) -> list[PlayerListResponse]:

    query = db.query(Player).order_by(Player.username.asc())

    filters = []
    if search_by_player:
        filters.append(Player.username.ilike(f"%{search_by_player}%"))
    if search_by_team:
        filters.append(Player.team.has(name=search_by_team))
    if filters:
        query = query.filter(*filters)

    query = query.offset(pagination.offset).limit(pagination.limit)

    db_players = query.all()

    sorted_players = sorted(
        db_players,
        key=lambda player: (
            player.won_games / player.played_games if player.played_games > 0 else 0
        ),
        reverse=(sort_by == "desc"),
    )

    return [convert_db_to_player_list_response(player) for player in sorted_players]


def get_player(db: Session, player_id: UUID) -> PlayerDetailResponse:
    db_player = v.player_exists(db, player_id)

    tournament_title = None
    if db_player.team_id and db_player.team.tournament_id:
        tournament_title = db_player.team.tournament.title

    return convert_db_to_player_detail_response(db_player, tournament_title)


def update_player(
    db: Session,
    player_id: UUID,
    player: PlayerUpdate,
    avatar: UploadFile | None,
    current_user: UserResponse
) -> PlayerListResponse:

    db_player = v.player_exists(db, player_id=player_id)

    if db_player.user_id:
        v.player_update_current_user_authorization(db_player, current_user)
    else:
        v.director_or_admin(current_user)

    if player.username:
        v.player_username_unique(db, username=player.username)
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

    if avatar:
        if db_player.avatar:
            s3_service.delete_file(str(db_player.avatar))

        avatar_url = s3_service.upload_file(avatar, "players")
        db_player.avatar = avatar_url

    db.commit()
    db.refresh(db_player)

    return convert_db_to_player_list_response(db_player)
