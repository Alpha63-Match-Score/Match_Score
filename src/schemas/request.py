from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field
from sqlalchemy import UUID

from src.models.enums import RequestStatus, RequestType

#
# class RequestBase(BaseModel):
#     response_date: Optional[str] = None
#     user_id: UUID
#     request_type: RequestType
#     player_id: Optional[UUID] = None
#     admin_id: Optional[UUID] = None
#
#     class Config:
#         orm_mode = True
#
#
# class LinkUserToPlayer(BaseModel):
#     player_id: UUID
#     admin_id: UUID
#     request_type: RequestType = RequestType.LINK_USER_TO_PLAYER
#     status: RequestStatus
#     # response_date: datetime = datetime.now()
#
#
# class PromoteUserToDirector(BaseModel):
#     user_id: UUID
#     admin_id: UUID
#     request_type: RequestType = RequestType.PROMOTE_USER_TO_DIRECTOR
#     status: RequestStatus
#     # response_date: datetime = datetime.now()
