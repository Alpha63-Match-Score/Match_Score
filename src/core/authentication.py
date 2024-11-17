from datetime import timedelta, datetime, timezone
from typing import Type

from fastapi import HTTPException, status
from jose import jwt
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.security import verify_password
from src.models.user import User
from src.utils import validators as v


def authenticate_user(
        db: Session,
        email: str,
        password: str
) -> Type[User]:

    user = db.query(User).filter(User.email == email).first()

    v.user_exists(db, user.id)

    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password")

    return user

def create_access_token(data: dict) -> str:

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRATION)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return encoded_jwt
