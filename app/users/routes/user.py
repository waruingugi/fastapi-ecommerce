from fastapi import Depends, APIRouter
from app.users.serializers.user import (
    UserInDBSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
)
from sqlalchemy.orm import Session
from app.core.deps import get_db, Permissions, get_current_active_user
from app.users.daos.user import user_dao
from typing import Any, List
from app.exceptions.custom import UserAlreadyExists
from app.users.filters import UserFilter
from app.users.permissions import UserPermissions
from app.users.models import User
from app.core.logger import LoggingRoute
from fastapi_sqlalchemy_filter import FilterDepends
from fastapi_pagination import Params

router = APIRouter(route_class=LoggingRoute)


@router.get("/users/me", response_model=UserInDBSerializer)
async def read_user_me(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
) -> Any:
    """Get current user"""
    return user_dao.get(db, id=user.id)


@router.patch("/users/me", response_model=UserInDBSerializer)
async def update_user_me(
    user_in: UserUpdateSerializer,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
) -> Any:
    """Update user me"""
    # Get the business_partner to be updated
    db_obj = user_dao.get(db, id=user.id)

    return user_dao.update(db, db_obj=db_obj, obj_in=user_in.dict(exclude_unset=True))


@router.get("/users", response_model=List[UserInDBSerializer])
async def read_users(
    params: Params = Depends(),
    user_filter: UserFilter = FilterDepends(UserFilter),
    db: Session = Depends(get_db),
    _: Permissions = Depends(Permissions(UserPermissions.user_read)),
) -> Any:
    """Get all users"""
    user_filter_dict = user_filter.dict()

    if not any(user_filter_dict.values()):  # Returns True if all values are falsy/None
        return user_dao.get_all(db)

    return user_dao.get_multi_paginated(db, user_filter, params)


@router.patch("/users/{user_id}", response_model=UserInDBSerializer)
async def update_user(
    user_id: str,
    user_in: UserUpdateSerializer,
    db: Session = Depends(get_db),
    _: Permissions = Depends(Permissions(UserPermissions.user_update)),
) -> Any:
    """Update user me"""
    # Get the business_partner to be updated
    db_obj = user_dao.get(db, id=user_id)

    return user_dao.update(db, db_obj=db_obj, obj_in=user_in.dict(exclude_unset=True))


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
        raise UserAlreadyExists

    user = user_dao.create(db, obj_in=user_data)
    return user
