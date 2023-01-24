from pydantic import BaseSettings
from functools import lru_cache
from sqlalchemy.engine import URL
from pydantic import (
    BaseSettings,
    PostgresDsn,
)


class Settings(BaseSettings):
    SECRET_KEY : str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRY_IN_SECONDS: int = 60 * 60 * 24

    SQLALCHEMY_DATABASE_URI: PostgresDsn = None
    ASYNC_SQLALCHEMY_DATABASE_URI: PostgresDsn = None

    SUPERUSER_FIRST_NAME: str
    SUPERUSER_LAST_NAME: str
    SUPERUSER_EMAIL: str
    SUPERUSER_PASSWORD: str
    SUPERUSER_PHONE: str

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_app_settings():
    return Settings()


settings = Settings()
