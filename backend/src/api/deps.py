from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from src.core.authentication import is_token_blacklisted
from src.core.config import settings
from src.crud.user import get_by_id
from src.database.session import SessionLocal
from src.models import User
from src.schemas.user import UserResponse


def get_db() -> Generator:
    """
    Get a database connection from the connection
    pool and return it to the pool when the request is finished.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/login")


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> UserResponse:

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    if is_token_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is logged out. Please log in again.",
        )

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_identifier: str = payload.get("user_id")
        if user_identifier is None:
            raise credential_exception

    except JWTError:
        raise credential_exception

    user = get_by_id(db, str(user_identifier))

    return convert_db_to_user_response(user)


def convert_db_to_user_response(user: User) -> UserResponse:
    return UserResponse(id=user.id, email=user.email, role=user.role)
