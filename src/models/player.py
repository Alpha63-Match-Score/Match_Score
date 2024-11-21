from src.models.base import Base, BaseMixin

from sqlalchemy import UUID, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Player(Base, BaseMixin):
    """
    Database model representing "player" table in the database.
    UUID and table name are inherited from BaseMixin.
    """

    username = Column(String(45), nullable=False, unique=True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    country = Column(String(45), nullable=False)
    avatar = Column(String(45), nullable=True)
    played_games = Column(Integer, nullable=False, default=0)
    won_games = Column(Integer, nullable=False, default=0)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)
    # user = relationship("User", back_populates="player")
    user = relationship(
        "User", back_populates="player", uselist=False, single_parent=True
    )

    team_id = Column(UUID(as_uuid=True), ForeignKey("team.id"), nullable=True)
    team = relationship("Team", back_populates="players")

    requests = relationship("Request", back_populates="player")
