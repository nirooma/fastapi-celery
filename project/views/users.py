from fastapi import APIRouter


views = APIRouter()


@views.get("/")
async def users():
    return "all_users"





