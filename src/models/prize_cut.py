from src.models.base import Base, BaseMixin

from sqlalchemy import UUID, Column, Float, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship


class PrizeCut(Base, BaseMixin):
    """
    Database model representing "prize_cut" table in the database.
    UUID and table name are inherited from BaseMixin.
    """

    place = Column(Integer, nullable=False)
    prize_cut = Column(Float, nullable=False)

    tournament_id = Column(
        UUID(as_uuid=True), ForeignKey("tournament.id"), nullable=False
    )
    tournament = relationship("Tournament", back_populates="prize_cuts")

    team_id = Column(
        UUID(as_uuid=True), ForeignKey("team.id"), nullable=True, default=None
    )
    team = relationship("Team", back_populates="prize_cuts")

    # Unique constraint to prevent
    # multiple prize cuts for the same place in the same tournament.
    __table_args__ = (UniqueConstraint("tournament_id", "place"),)
