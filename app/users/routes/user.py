from fastapi import Depends, APIRouter
from app.users.serializers.user import UserInDBSerializer, UserCreateSerializer
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.users.daos.user import user_dao
from typing import Any, List
from app.exceptions.custom import HttpErrorException
from http import HTTPStatus
from app.errors.custom import ErrorCodes
from app.users.filters import UserFilter
from app.core import deps
from app.users.models import User
from app.core.logger import LoggingRoute
from fastapi_sqlalchemy_filter import FilterDepends
from fastapi_pagination import Params

router = APIRouter(route_class=LoggingRoute)


@router.get("/users/me", response_model=UserInDBSerializer)
async def read_user_me(
    db: Session = Depends(get_db),
) -> Any:
    """Get current user"""
    return user_dao.get(db, phone="+254701023045")


@router.get("/users", response_model=List[UserInDBSerializer])
async def read_users(
    params: Params = Depends(),
    user_filter: UserFilter = FilterDepends(UserFilter),
    db: Session = Depends(get_db),
    _: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """Get all users"""
    user_filter_dict = user_filter.dict()

    if not any(user_filter_dict.values()):  # Returns True if all values are falsy/None
        return user_dao.get_all(db)

    return user_dao.get_multi_paginated(db, user_filter, params)


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
