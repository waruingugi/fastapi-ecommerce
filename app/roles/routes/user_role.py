from app.core.deps import get_db, Permissions, get_current_active_superuser
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.roles.serializers.user_role import (
    UserRoleUpdateSerializer,
    UserRoleInDBSerializer,
)
from app.users.models import User
from typing import List
from app.roles.daos.user_role import user_role_dao
from app.roles.permissions import UserRolePermissions
from app.core.logger import LoggingRoute
from app.roles.filters import UserRoleFilter
from fastapi_sqlalchemy_filter import FilterDepends

router = APIRouter(route_class=LoggingRoute)


@router.post("/", response_model=UserRoleInDBSerializer)
async def create_user_role(
    role_in: UserRoleUpdateSerializer,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_superuser),
):
    """Create user role"""
    return user_role_dao.get_or_create(db, obj_in=role_in)


@router.get("/roles", response_model=List[UserRoleInDBSerializer])
async def read_user_roles(
    user_role_filter: UserRoleFilter = FilterDepends(UserRoleFilter),
    db: Session = Depends(get_db),
    _: Permissions = Depends(Permissions(UserRolePermissions.user_role_list)),
):
    """Read user roles"""
    user_role_filter_dict = user_role_filter.dict()

    if not any(
        user_role_filter_dict.values()
    ):  # Returns True if all values are falsy/None
        return user_role_dao.get_all(db)

    return user_role_dao.search(db, user_role_filter)


# Search query
# - Scope, create model country
# - Celery
# Redis
