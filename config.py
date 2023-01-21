from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    SECRET_KEY : str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRY_IN_SECONDS: int = 60 * 60 * 24

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
