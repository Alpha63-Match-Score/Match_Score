
from pydantic import BaseModel, EmailStr, Field, field_validator
from uuid import UUID

from starlette import status
from starlette.exceptions import HTTPException


class UserBase(BaseModel):
    id: UUID
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str = Field(
        min_length=4,
        max_length=36,
        examples=["Example123@"]
    )

    @field_validator('password')
    def validate_password(cls, value):
        validate = lambda pwd: (
                any(c.isupper() for c in pwd) and
                any(c.islower() for c in pwd) and
                any(c.isdigit() for c in pwd) and
                any(c in '@$!%*?&' for c in pwd) and
                not any(c.isspace() for c in pwd)
        )

        if not validate(value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one uppercase letter, one lowercase letter, "
                       "one number, and one special character and must not contain any spaces"
            )
        return value


class UserUpdateRole(BaseModel):
    role: str


class UserConnectPlayer(BaseModel):
    player_id: UUID
