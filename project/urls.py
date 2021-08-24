from fastapi import APIRouter

from project.routers import users

api_routers = APIRouter()

api_routers.include_router(prefix="/users", router=users.router, tags=["users"])
