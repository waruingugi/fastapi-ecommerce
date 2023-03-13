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
from app.core.deps import RestrictUserFilter

router = APIRouter(route_class=LoggingRoute)


@router.get("/me", response_model=UserInDBSerializer)
async def read_user_me(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
) -> Any:
    """Get current user"""
    return user_dao.get(db, id=user.id)


@router.patch("/me", response_model=UserInDBSerializer)
async def update_user_me(
    user_in: UserUpdateSerializer,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_active_user),
) -> Any:
    """Update user me"""
    # Get the user to be updated
    db_obj = user_dao.get_not_none(db, id=user.id)

    return user_dao.update(db, db_obj=db_obj, obj_in=user_in.dict(exclude_unset=True))


@router.get("/", response_model=List[UserInDBSerializer])
async def read_users(
    params: Params = Depends(),
    user_filter: UserFilter = FilterDepends(UserFilter),
    db: Session = Depends(get_db),
    _: Permissions = Depends(Permissions(UserPermissions.user_read)),
    restrict_user_filter: RestrictUserFilter = Depends(RestrictUserFilter),
) -> Any:
    """Get all users"""
    user_filter_dict = user_filter.dict()
    search_filter = restrict_user_filter(search_filter=user_filter)

    if not any(user_filter_dict.values()):  # Returns True if all values are falsy/None
        return user_dao.get_all(db)

    return user_dao.search(db, search_filter)


@router.patch("/{user_id}", response_model=UserInDBSerializer)
async def update_user(
    user_id: str,
    user_in: UserUpdateSerializer,
    db: Session = Depends(get_db),
    _: Permissions = Depends(Permissions(UserPermissions.user_update)),
) -> Any:
    """Update user"""
    # Get the user to be updated
    db_obj = user_dao.get_not_none(db, id=user_id)

    return user_dao.update(db, db_obj=db_obj, obj_in=user_in)


@router.post("/register/", response_model=UserInDBSerializer)
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
