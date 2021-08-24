import datetime
import logging
import os

from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse

from project.celery.celery_utils import create_celery

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

    @app.on_event("startup")
    async def startup_event():
        logger.info("initialize database...")
        init_db(app)
        logger.info("initialization database success")

    @app.get("/health_check")
    async def health_check(
        request: Request, settings: BaseConfig = Depends(get_settings)
    ):
        return JSONResponse(
            {
                "status": status.HTTP_200_OK,
                "timestamp": datetime.datetime.now().isoformat(),
                "container": os.uname()[1],
                "path": request.scope.get("path"),
                "environment": settings.ENVIRONMENT,
                "debugMode": settings.DEBUG,
            }
        )

    return app
