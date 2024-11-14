from sqlalchemy import Column, String, Enum, DateTime, Integer, UUID, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.models.base import Base, BaseMixin
from src.models.enums import MatchFormat, Stage


class Match(Base, BaseMixin):
    """
    Database model representing "match" table in the database.
    UUID and table name are inherited from BaseMixin.
    """

    match_format = Column(Enum(MatchFormat), nullable=False)
    start_time = Column(DateTime, nullable=False)
    is_finished = Column(Boolean, nullable=False, default=False)
    stage = Column(Enum(Stage), nullable=False)

    team1_id = Column(UUID(as_uuid=True), ForeignKey("team.id"), nullable=False)
    team2_id = Column(UUID(as_uuid=True), ForeignKey("team.id"), nullable=False)

    team1 = relationship("Team", foreign_keys=[team1_id])
    team2 = relationship("Team", foreign_keys=[team2_id])

    team1_score = Column(Integer, default=0)
    team2_score = Column(Integer, default=0)

    tournament_id = Column(UUID(as_uuid=True), ForeignKey("tournament.id"), nullable=False)
    tournament = relationship("Tournament", back_populates="matches")
