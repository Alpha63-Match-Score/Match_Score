from fastapi import APIRouter

from src.api.v1.endpoints import users
from src.api.v1.endpoints import matches
from src.api.v1.endpoints import tournaments

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(matches.router, prefix="/matches", tags=["matches"])
api_router.include_router(tournaments.router, prefix="/tournaments", tags=["tournaments"])

