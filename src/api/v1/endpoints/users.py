from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.api.deps import get_db, get_current_user
from src.core.authentication import authenticate_user, create_access_token
from src.crud.user import create_user, update_email
from src.models import User
from src.schemas.schemas import Token, UserResponse, UserCreate, UserUpdate

router = APIRouter()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(user, db)
    return UserResponse(email=db_user.email, role=db_user.role)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token = create_access_token(data={"user_id": str(user.id)})
    return Token(access_token=access_token, token_type="bearer")


@router.put("/update")
def update_user(user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    msg = update_email(db, user.email, current_user)
    return msg


# TODO eventually add logout

