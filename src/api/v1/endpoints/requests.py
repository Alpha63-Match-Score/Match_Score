from typing import Literal

from src.api.deps import get_current_user, get_db
from src.crud.request import (
    get_all,
    send_director_request,
    send_link_to_player_request,
    update_request,
)
from src.models import User
from src.utils.pagination import PaginationParams, get_pagination

from fastapi import APIRouter, Depends
from fastapi.params import Path
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/directors/{user_id}")
def director_request(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return send_director_request(db, current_user)


@router.post("/players/{username}")
def player_request(
    username: str = Path(description="player_username"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return send_link_to_player_request(db, current_user, username)


@router.get("/")
def get_all_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    sort_by: Literal["asc", "desc"] = "desc",
    status: Literal["pending", "accepted", "rejected"] | None = None,
    request_type: (
        Literal["link user to player", "promote user to director"] | None
    ) = None,
    filter_by_current_admin: bool = False,
    pagination: PaginationParams = Depends(get_pagination),
):
    return get_all(
        db,
        current_user,
        pagination,
        sort_by,
        status,
        request_type,
        filter_by_current_admin,
    )


@router.put("/{request_id}")
def put_request(
    status: Literal["accepted", "rejected"],
    email: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_request(db, current_user, status, email)
