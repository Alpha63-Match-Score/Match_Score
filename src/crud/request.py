from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import asc, desc, UUID
from sqlalchemy.orm import Session
from src.utils.pagination import PaginationParams
from src.models import Request, User, Player
from src.models.enums import RequestType, Role, RequestStatus
from src.schemas.schemas import ResponseRequest, RequestListResponse
from src.utils.validators import player_exists, user_role_is_admin, \
    request_exists, user_exists, user_role_is_user, get_user_by_email
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
            email=request.user.email,
            request_type=request.request_type,
            status=request.status,
            request_date=request.request_date,
            response_date=request.response_date,
            admin_id=request.admin_id,
            username=request.username
        )
        for request in query
    ]
    return result


def send_director_request(db: Session, current_user: User):

    user_role_is_user(current_user)
    check_valid_request(db, current_user)

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
        status=db_request.status,
        response_date=db_request.response_date
    )


def send_link_to_player_request(db: Session, current_user: User, username: str):

    user_role_is_user(current_user)
    player_exists(db, username)
    check_valid_request(db, current_user)

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
        status=db_request.status,
        response_date=db_request.response_date
    )


def check_valid_request(db: Session, current_user: User):
    request = db.query(Request).filter(Request.user_id == current_user.id).first()
    if request and request.status == RequestStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already have a pending request."
        )


def update_request(db: Session,
                   current_user: User,
                   status: Literal['accepted', 'rejected'],
                   email: str):
    user_role_is_admin(current_user)
    user = get_user_by_email(db, email)
    request = request_exists(db, user)
    check_request_status(request)

    if request.request_type == RequestType.LINK_USER_TO_PLAYER:
        player = player_exists(db, request.username)
        pass
    elif request.request_type == RequestType.PROMOTE_USER_TO_DIRECTOR:
        return get_director_requests(db, current_user, status, request)


def get_director_requests(db, admin: User, status: str, request: Request):
    user_id = request.user_id
    user = user_exists(db, user_id)

    if status == RequestStatus.ACCEPTED:
        return accept_director_request(db, admin, user, request)
    elif status == RequestStatus.REJECTED:
        return reject_director_request(db, admin, request)


def accept_director_request(db, admin: User, user: User, request: Request):
    request.status = RequestStatus.ACCEPTED
    request.admin_id = admin.id
    request.response_date = datetime.now()
    user.role = Role.DIRECTOR
    db.commit()
    db.refresh(request)
    db.refresh(user)

    return ResponseRequest(
        request_type=request.request_type,
        request_date=request.request_date,
        status=request.status,
        response_date=request.response_date,
    )


def reject_director_request(db, admin: User, request: Request):
    request.status = RequestStatus.REJECTED
    request.admin_id = admin.id
    request.response_date = datetime.now()
    db.commit()
    db.refresh(request)

    return ResponseRequest(
        request_type=request.request_type,
        request_date=request.request_date,
        status=request.status,
        response_date=request.response_date,
    )


def check_request_status(request: Request):
    if request.response_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request has already been responded to."
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
