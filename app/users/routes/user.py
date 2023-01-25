import fastapi
from fastapi import Depends
from sqlalchemy.orm import Session
from app.users.serailizers.users import UserInDBSerializer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_async_db
from app.users.daos.user import UserDao


router = fastapi.APIRouter()


@router.get("/", response_model=UserInDBSerializer)
async def read_users(
    db: AsyncSession = Depends(get_async_db),
    user_dao: Depends(UserDao)
):
    """Retrieve users"""
    pass
