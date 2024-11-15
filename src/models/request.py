from sqlalchemy import Column, String, Enum, DateTime, ForeignKey, UUID
from sqlalchemy.orm import relationship

from src.models.base import Base, BaseMixin
from src.models.enums import RequestStatus, RequestType


class Request(Base, BaseMixin):
    """
    Database model representing "user" table in the database.
    UUID and table name are inherited from BaseMixin.
    """
    status = Column(Enum(RequestStatus), nullable=False)
    request_date = Column(DateTime, nullable=False)
    response_date = Column(DateTime, nullable=False)
    request_type = Column(Enum(RequestType), nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    player_id = Column(UUID(as_uuid=True), ForeignKey("player.id"), nullable=True)
    admin_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="requests_user")
    player = relationship("Player", back_populates="requests")


