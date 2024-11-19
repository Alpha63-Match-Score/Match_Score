from fastapi import HTTPException, status
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from src.utils.pagination import PaginationParams
from src.models import Request, User, Player
from src.models.enums import RequestType
from src.schemas.schemas import ResponseRequest, RequestListResponse
from src.utils.validators import player_exists, user_role_is_director, user_role_is_player, user_role_is_admin
from typing import Literal


def get_all(
        db: Session,
        current_user: User,
        pagination: PaginationParams,
        sort_by: Literal['asc', 'desc'] = 'desc',
        status: Literal['pending', 'accepted', 'rejected'] | None = None,
        request_type: Literal['link user to player', 'promote user to director'] | None = None,
        filter_by_admin: bool = False,
        # request_date: str = None,
        # response_date: str = None,
):
    user_role_is_admin(current_user)
    query = db.query(Request)

    if status:
        query = query.filter(Request.status == status)

    if request_type:
        query = query.filter(Request.request_type == request_type)

    if filter_by_admin:
        query = query.filter(Request.admin_id == current_user.id)

    if sort_by == 'asc':
        query = query.order_by(asc(Request.request_date))
    elif sort_by == 'desc':
        query = query.order_by(desc(Request.request_date))

    # if response_date:
    #     query = query.filter(Request.response_date == response_date)

    query = query.offset(pagination.offset).limit(pagination.limit)

    result = [
        RequestListResponse(
            request_type=request.request_type,
            status=request.status,
            request_date=request.request_date,
            admin_id=request.admin_id
        )
        for request in query
    ]
    return result


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
