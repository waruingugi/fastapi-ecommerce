from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    AsyncSession
)
from app.core.config import get_app_settings
from functools import lru_cache
from sqlalchemy.engine import Engine


lru_cache
def get_engine() -> Engine:
    settings = get_app_settings()
    return create_engine(
        settings.SQLALCHEMY_DATABASE_URI,
        future=True,
        echo=True,
        pool_pre_ping=True,
        connect_args={
            "application_name": "api",
            "options": "-c statement_timeout=10000 -c idle_in_transaction_session_timeout=60000",
        },
    )

## Check class type
lru_cache
def get_async_engine() -> AsyncEngine:
    settings = get_app_settings()
    return create_async_engine(
        settings.ASYNC_SQLALCHEMY_DATABASE_URI,
        pool_pre_ping=True,
        echo=True,
        connect_args={
            "server_settings": {
                "application_name": "api",
                "statement_timeout": "10000",
                "idle_in_transaction_session_timeout": "60000",
            },
            "command_timeout": 10,
        },
    )


def get_session() -> sessionmaker:
    return sessionmaker(
        autocommit=False, autoflush=False, bind=get_engine(), future=True
    )


def get_async_session() -> sessionmaker:
    return sessionmaker(
        get_async_engine(), class_=AsyncSession, expire_on_commit=False
    )
