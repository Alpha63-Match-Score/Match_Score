from src.models.base import Base, BaseMixin
from src.models.enums import Role

from sqlalchemy import Column, DateTime, Enum, String, func
from sqlalchemy.orm import relationship


class User(Base, BaseMixin):
    """
    Database model representing "user" table in the database.
    UUID and table name are inherited from BaseMixin.
    """

    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(Role), default=Role.USER, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # player_id = Column(UUID(as_uuid=True), ForeignKey("player.id"), nullable=True)

    requests_user = relationship(
        "Request", back_populates="user", foreign_keys="[Request.user_id]"
    )
    requests_admin = relationship(
        "Request", back_populates="admin", foreign_keys="[Request.admin_id]"
    )

    tournaments = relationship("Tournament", back_populates="director")
    # player = relationship("Player", back_populates="user")
    player = relationship(
        "Player", back_populates="user", uselist=False, foreign_keys="[Player.user_id]"
    )
