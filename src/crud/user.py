from src.core.security import get_password_hash
from src.models.user import User
from src.schemas.schemas import UserCreate, UserResponse
from src.utils.validators import user_email_exists

from fastapi import HTTPException, status
from sqlalchemy.orm import Session


def create_user(user: UserCreate, db: Session):
    user_email_exists(db, user.email)
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        password_hash=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_by_id(db: Session, user_id: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    return user


def update_email(db: Session, email: str, current_user: User):
    user_email_exists(db, email)
    user = db.query(User).filter(User.id == current_user.id).first()

    user.email = email
    db.commit()
    db.refresh(user)
    return {"message": "Email updated successfully."}


def convert_db_to_user_response(user: User) -> UserResponse:
    return UserResponse(id=user.id, email=user.email, role=user.role)
