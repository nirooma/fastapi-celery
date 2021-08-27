import os
import pathlib
from functools import lru_cache


class BaseConfig:
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent
    DATABASE_URL: str = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR}/db.sqlite3"
    )
    # DATABASE_URL = f"sqlite:///{BASE_DIR}/db.sqlite3"
    DEBUG: bool = os.environ.get("DEBUG", True)
    SECRET_KEY = os.environ.get("SECRET_KEY", "SOME_RANDOM_SECRET")

    # Celery
    broker_url: str = os.environ.get("CELERY_BROKER_URL", "amqp://localhost:5672")
    result_backend: str = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

    # Celery Beat
    beat_schedule: dict = {
        "test_connection": {
            "task": "check_connection",
            "schedule": 60,  # five seconds
        },
    }

    def __str__(self):
        return f"{self.__class__.__name__}"


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }

    config_name = os.environ.get("FASTAPI_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
