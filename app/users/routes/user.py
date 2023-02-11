import fastapi
from fastapi import Depends
from sqlalchemy.orm import Session
from app.users.serializers.user import UserInDBSerializer, UserCreateSerializer
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.users.daos.user import user_dao
from typing import Any, List
from app.exceptions.custom import HttpErrorException
from http import HTTPStatus
from app.errors.custom import ErrorCodes


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


@router.post("/register/user", response_model=UserInDBSerializer)
def register_user(
    user_data: UserCreateSerializer,
    db: Session = Depends(get_db),
) -> Any:
    """Create new user"""
    user_in = user_dao.get_by_phone_or_email(
        db, email=user_data.email, phone=user_data.phone
    )

    if user_in:
        raise HttpErrorException(
            status_code=HTTPStatus.BAD_REQUEST,
            error_code=ErrorCodes.USERNAME_ALREADY_EXISTS.name,
            error_message=ErrorCodes.USERNAME_ALREADY_EXISTS.value,
        )

    user = user_dao.create(db, obj_in=user_data)
    return user
