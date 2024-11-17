from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.deps import get_current_user, get_db
from src.crud.request import send_director_request
from src.models import User

router = APIRouter()


@router.post("/users/{user_id}")
def director_request(db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    return send_director_request(db, current_user)
