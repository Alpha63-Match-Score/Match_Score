from sqlalchemy import Column, String, Integer, UUID, ForeignKey
from sqlalchemy.orm import relationship

from src.models.base import BaseMixin, Base


class Team(Base, BaseMixin):
    """
    Database model representing "team" table in the database.
    UUID and table name are inherited from BaseMixin.
    """

    name = Column(String(45), nullable=False, unique=True)
    logo = Column(String(45), nullable=True)
    played_games = Column(Integer, nullable=False, default=0)
    won_games = Column(Integer, nullable=False, default=0)
    tournament_id = Column(
        UUID(as_uuid=True), ForeignKey("tournament.id"), nullable=True
    )

    players = relationship("Player", back_populates="team")
    # matches = relationship("Match", back_populates="team")
    matches_as_team1 = relationship(
        "Match", foreign_keys="[Match.team1_id]", back_populates="team1"
    )
    matches_as_team2 = relationship(
        "Match", foreign_keys="[Match.team2_id]", back_populates="team2"
    )
    prize_cuts = relationship("PrizeCut", back_populates="team")
    tournament = relationship("Tournament", back_populates="teams")

    wins = relationship(
        "Match", foreign_keys="[Match.winner_team_id]", back_populates="winner_team"
    )
