import logging

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise, run_async
from .config import settings

logger = logging.getLogger(__name__)

TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": ["project.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def init_db(app: FastAPI) -> None:
    logger.info("Initialization database connection")
    register_tortoise(
        app,
        db_url=settings.DATABASE_URL,
        modules={"models": ["project.models"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )


async def generate_schema() -> None:

    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        # modules={"models": ["models.tortoise"]},
        modules={"models": ["project.models"]},
    )
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


if __name__ == "__main__":
    run_async(generate_schema())
