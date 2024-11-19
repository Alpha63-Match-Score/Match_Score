from typing import Literal

from fastapi import APIRouter, Depends
from fastapi.params import Path
from sqlalchemy.orm import Session

from src.api.deps import get_current_user, get_db
from src.crud.request import send_director_request, send_link_to_player_request, get_all
from src.models import User
from src.utils.pagination import PaginationParams, get_pagination

router = APIRouter()


@router.post("/users/{user_id}")
def director_request(db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)
                     ):
    return send_director_request(db, current_user)


@router.post("/users/{user_id}/players/{username}")
def player_request(username: str = Path(description="player_username"),
                   db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user),
                   ):
    return send_link_to_player_request(db, current_user, username)


@router.get("/users")
def get_all_requests(db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user),
                     sort_by: Literal['acs', 'desc'] = 'desc',
                     status: Literal['pending', 'accepted', 'rejected'] | None = None,
                     request_type: Literal['link user to player', 'promote user to director'] | None = None,
                     filter_by_current_admin: bool = False,
                     pagination: PaginationParams = Depends(get_pagination)
                     ):
    return get_all(db, current_user, pagination, sort_by, status, request_type, filter_by_current_admin)

