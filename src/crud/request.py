from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models import Request, User, Player
from src.models.enums import RequestType
from src.schemas.schemas import ResponseRequest
from src.utils.validators import player_exists, user_role_is_director, user_role_is_player


def send_director_request(db: Session, current_user: User):

    user_role_is_director(current_user)
    user_role_is_player(current_user)

    db_request = Request(
        user_id=current_user.id,
        request_type=RequestType.PROMOTE_USER_TO_DIRECTOR
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return ResponseRequest(
        request_type=db_request.request_type,
        request_date=db_request.request_date,
        status=db_request.status
    )


def get_director_requests():
    """Get all director requests."""
    pass


def accept_director_request():
    """Change the status of the request to accepted."""
    pass


def reject_director_request():
    """Change the status of the request to rejected."""
    pass


def send_link_to_player_request(db: Session, current_user: User, username: str):

    player_exists(db, username)
    user_role_is_director(current_user)
    user_role_is_player(current_user)

    db_request = Request(
        user_id=current_user.id,
        request_type=RequestType.LINK_USER_TO_PLAYER,
        username=username
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return ResponseRequest(
        request_type=db_request.request_type,
        request_date=db_request.request_date,
        status=db_request.status
    )


def get_link_to_player_requests():
    """Get all link to player requests."""
    pass


def accept_link_to_player_request():
    """Change the status of the request to accepted."""
    pass


def reject_link_to_player_request():
    """Change the status of the request to rejected."""
    pass

# HELPER METHODS //
# get_director_request_by_id
# get_link_to_player_request_by_id
# update_director_request_status
# update_link_to_player_request_status
# update_user_to_player
# link_user_to_player
