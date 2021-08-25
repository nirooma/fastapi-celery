from fastapi import APIRouter

from project.views import users

routers = APIRouter()

routers.include_router(prefix="/users", router=users.views, tags=["users"])
