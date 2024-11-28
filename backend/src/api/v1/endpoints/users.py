from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.api.deps import get_current_user, get_db, oauth2_scheme
from src.core.authentication import authenticate_user, create_access_token
from src.core.config import settings
from src.crud.user import create_user, update_email
from src.models import User
from src.schemas.user import Token, UserCreate, UserRegisterResponse, UserUpdate

router = APIRouter()


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(user, db)
    return UserRegisterResponse(email=db_user.email, role=db_user.role)


@router.post("/login", include_in_schema=False)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token = create_access_token(data={"user_id": str(user.id)})
    return Token(access_token=access_token, token_type="bearer", user_id=str(user.id), role=user.role)


@router.put("/update")
def update_user(
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    msg = update_email(db, user.email, current_user)
    return msg


# get or post?
@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    settings.BLACKLISTED_TOKENS.append(token)
    return {"message": "Logout successful."}

@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "role": current_user.role,
    }
