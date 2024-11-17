from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.models import Request, User, Player
from src.models.enums import RequestType
from src.schemas.schemas import PromoteUserToDirector


def send_director_request(db: Session, current_user: User):
    """Send a request to be a director. Has to be approved by the admin."""
    if current_user.role == "director":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User is already a director."
        )
    if current_user.role == "player":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User is already a player."
        )
    db_request = Request(
        user_id=current_user.id,
        request_type=RequestType.PROMOTE_USER_TO_DIRECTOR
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return PromoteUserToDirector(
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


def send_link_to_player_request(db: Session, current_user: User, player: Player):
    """Send a request to link to a player."""
    if current_user.role == "director":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User is already a director."
        )
    if current_user.role == "player":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User is already a player."
        )
    db_request = Request(
        user_id=current_user.id,
        request_type=RequestType.LINK_USER_TO_PLAYER,
        player=player.username

    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return PromoteUserToDirector(
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
