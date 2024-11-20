from src.models.base import Base, BaseMixin
from src.models.enums import RequestStatus, RequestType

from sqlalchemy import UUID, Column, DateTime, Enum, ForeignKey, String, func
from sqlalchemy.orm import relationship


class Request(Base, BaseMixin):
    """
    Database model representing "user" table in the database.
    UUID and table name are inherited from BaseMixin.
    """

    status = Column(Enum(RequestStatus), nullable=False, default=RequestStatus.PENDING)
    request_date = Column(DateTime, default=func.now(), nullable=False)
    response_date = Column(DateTime, nullable=True)
    request_type = Column(Enum(RequestType), nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    # player_id = Column(UUID(as_uuid=True), ForeignKey("player.id"), nullable=True)
    username = Column(String(45), ForeignKey("player.username"), nullable=True)
    admin_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)

    user = relationship("User", back_populates="requests_user", foreign_keys=[user_id])
    admin = relationship(
        "User", back_populates="requests_admin", foreign_keys=[admin_id]
    )

    player = relationship("Player", back_populates="requests")
