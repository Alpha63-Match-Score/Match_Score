from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from src.core.config import settings
from src.crud.user import get_by_id
from src.database.session import SessionLocal


def get_db() -> Generator:
    """
    Get a database connection from the connection pool and return it to the pool when the request is finished.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

def get_current_user(db: Session = Depends(get_db),
                     token: str = Depends(oauth2_scheme)):

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials")

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_identifier: str = payload.get("user_id")
        if user_identifier is None:
            raise credential_exception

    except JWTError:
        raise credential_exception

    user = get_by_id(db, int(user_identifier))

    return user