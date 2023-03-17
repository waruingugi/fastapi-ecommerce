from functools import lru_cache
from pydantic import BaseSettings, PostgresDsn, EmailStr
from typing import cast
from redis import Redis


class Settings(BaseSettings):
    PROJECT_NAME: str = "Ecommerce API"
    API_VERSION: str = "0.0.1"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRY_IN_SECONDS: int = 60 * 60 * 24
    REFRESH_TOKEN_EXPIRY_IN_SECONDS: int = 60 * 60 * 7

    SQLALCHEMY_DATABASE_URI: PostgresDsn = None
    ASYNC_SQLALCHEMY_DATABASE_URI: PostgresDsn = None

    SUPERUSER_FIRST_NAME: str
    SUPERUSER_LAST_NAME: str
    SUPERUSER_EMAIL: EmailStr
    SUPERUSER_PASSWORD: str
    SUPERUSER_PHONE: str

    REDIS_HOST: str = "localhost"
    REDIS_PASSWORD: str | None
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_app_settings() -> Settings:
    return Settings()  # type: ignore


# settings = Settings()
settings = cast(Settings, get_app_settings())


@lru_cache
def get_redis() -> Redis:
    return Redis(
        host=settings.REDIS_HOST or "localhost",
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        db=settings.REDIS_DB,
        decode_responses=True,
    )


# settings = Settings()
redis = cast(Redis, get_redis())
