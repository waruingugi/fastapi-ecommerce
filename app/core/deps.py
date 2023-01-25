from typing import Generator, AsyncGenerator

from app.db.session import SessionLocal, AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncEngine

def get_db() -> Generator:
    with SessionLocal() as db:
        yield db


async def get_async_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as db:
        yield db
