from sqlalchemy import Column, String, Enum, DateTime, Integer, UUID, ForeignKey
from sqlalchemy.orm import relationship

from src.models.base import Base, BaseMixin
from src.models.enums import TournamentFormat, Stage


class Tournament(Base, BaseMixin):
    """
    Database model representing "tournament" table in the database.
    UUID and table name are inherited from BaseMixin.
    """

    title = Column(String(45), unique=True, nullable=False)
    tournament_format = Column(Enum(TournamentFormat), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    prize_pool = Column(Integer, nullable=False)
    current_stage = Column(Enum(Stage), nullable=False)

    director_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    director = relationship("User", back_populates="tournaments")

    matches = relationship("Match", back_populates="tournament")
    prize_cuts = relationship("PrizeCut", back_populates="tournament")


