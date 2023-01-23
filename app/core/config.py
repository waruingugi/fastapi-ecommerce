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
    DATABASE_DRIVER_NAME: str = "postgresql"
    SQLALCHEMY_DATABASE_URI: PostgresDsn = None
    ASYNC_SQLALCHEMY_DATABASE_URI: PostgresDsn = None


    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_app_settings():
    return Settings()


settings = Settings()
