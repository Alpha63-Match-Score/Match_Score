from typing import Type
from uuid import UUID

from dns.e164 import query
from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from starlette.status import HTTP_400_BAD_REQUEST
from src.utils import validators as v
from src.models import Player

from src.schemas.schemas import UserResponse, PlayerCreate, \
    PlayerListResponse
from src.utils import validators as v
from src.utils.pagination import PaginationParams


def create_player( db: Session, player: PlayerCreate, current_user: UserResponse)-> PlayerListResponse:
    v.player_exists(db, username=player.username)
    v.director_or_admin(current_user)

    db_player = Player(
        username=player.username,
        first_name=player.first_name,
        last_name=player.last_name,
        country=player.country,
        avatar=player.avatar
 )

    db.add(db_player)
    db.commit()
    db.refresh(db_player)

    return convert_db_to_player_list_response(db_player)

def convert_db_to_player_list_response(
        db_player: Type[Player]
) -> PlayerListResponse:
    return PlayerListResponse(
        id=db_player.id,
        username=db_player.username,
        first_name=db_player.first_name,
        last_name=db_player.last_name,
        country=db_player.country,
        avatar=db_player.avatar,
        team_id=db_player.team_id,
        user_id=db_player.user_id
    )