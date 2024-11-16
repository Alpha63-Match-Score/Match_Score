from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.api.deps import get_db
from src.core.authentication import authenticate_user, create_access_token
from src.crud.user import create_user
from src.schemas.schemas import Token, UserResponse, UserCreate

router = APIRouter()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(user, db)
    return UserResponse(email=db_user.email, role=db_user.role)


# TODO add logout
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token = create_access_token(data={"user_id": str(user.id)})
    return Token(access_token=access_token, token_type="bearer")


@router.put("/{user_id}")
def update_user(user_id: int):
    pass
