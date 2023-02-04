import fastapi
from fastapi import Depends
from sqlalchemy.orm import Session
from app.users.serializers.user import UserInDBSerializer
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.users.daos.user import user_dao
from typing import Any, List


router = fastapi.APIRouter()


@router.get("/", response_model=UserInDBSerializer)
async def get_all_users(
    db: Session = Depends(get_db),
) -> Any:
    """Retrieve users"""
    return user_dao.get_all(db)
