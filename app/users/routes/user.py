import fastapi
from fastapi import Depends
from sqlalchemy.orm import Session
from app.users.serializers.user import UserInDBSerializer
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.users.daos.user import user_dao
from typing import Any, List


router = fastapi.APIRouter()


@router.get("/users/me", response_model=UserInDBSerializer)
async def read_user_me(
    db: Session = Depends(get_db),
) -> Any:
    """Get current user"""
    return user_dao.get(db, phone="+254701023045")


@router.get("/users", response_model=List[UserInDBSerializer])
async def read_users(
    db: Session = Depends(get_db),
) -> Any:
    """Get all users"""
    return user_dao.get_all(db)
