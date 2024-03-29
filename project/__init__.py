import datetime
import logging
import os
import platform
from fastapi.responses import RedirectResponse
import psycopg2
from fastapi import Depends, FastAPI, Request, status, Response
from fastapi.responses import JSONResponse

from project.celery.celery_utils import create_celery
from project import urls

from .celery import tasks  # noqa
from .config import BaseConfig, get_settings
from .database import init_db

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI()

    # do this before loading routes
    app.celery_app = create_celery()

    # Settings Logging System
    from project.logging import configure_logging
    configure_logging()

    # route to urls
    app.include_router(prefix="/api/v1", router=urls.routers)

    @app.on_event("startup")
    async def startup_event():
        logger.info("initialize database...")
        try:
            init_db(app)
        except psycopg2.Error as error:
            logger.error("initialization database failed", exc_info=error)

    @app.get("/health_check")
    async def health_check(settings: BaseConfig = Depends(get_settings)):
        """ Internal use only - Do not use with a client API """

        return JSONResponse(
            {
                "status": status.HTTP_200_OK,
                "timestamp": datetime.datetime.now().ctime(),
                "debugMode": settings.DEBUG,
                "OperatingSystem": platform.uname()
            }
        )

    return app
