from fastapi import APIRouter

from project.models import User

router = APIRouter()


@router.get("/")
async def users():
    return "all_users"





