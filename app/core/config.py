from pydantic import BaseSettings
from functools import lru_cache
from sqlalchemy.engine import URL
from pydantic import (
    BaseSettings,
    PostgresDsn,
    EmailStr
)


class Settings(BaseSettings):
    PROJECT_NAME: str = "Ecommerce API"
    API_VERSION: str = "0.0.1"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY : str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRY_IN_SECONDS: int = 60 * 60 * 24

    SQLALCHEMY_DATABASE_URI: PostgresDsn = None
    ASYNC_SQLALCHEMY_DATABASE_URI: PostgresDsn = None

    SUPERUSER_FIRST_NAME: str
    SUPERUSER_LAST_NAME: str
    SUPERUSER_EMAIL: EmailStr
    SUPERUSER_PASSWORD: str
    SUPERUSER_PHONE: str

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_app_settings():
    return Settings()


settings = Settings()
