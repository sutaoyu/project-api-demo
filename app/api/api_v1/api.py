from fastapi import APIRouter
from app.api.api_v1.endpoints import tasks, clues, users, login, search

api_router = APIRouter()

api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(clues.router, prefix="/clues", tags=["clues"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
