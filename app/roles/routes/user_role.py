from app.core.deps import get_db, Permissions
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.roles.serializers.user_role import (
    UserRoleInDBSerializer,
    UserRoleCreateSerializer,
    UserRoleUpdateSerializer,
)
from app.users.models import User
from app.users.daos.user import user_dao
from app.roles.daos.role import role_dao
from sqlalchemy.orm import load_only
from typing import List
from app.roles.daos.user_role import user_role_dao
from app.roles.permissions import UserRolePermissions
from app.core.logger import LoggingRoute
from app.roles.filters import UserRoleFilter
from fastapi_sqlalchemy_filter import FilterDepends
from typing import Any

router = APIRouter(route_class=LoggingRoute)


@router.post("/user-role", response_model=UserRoleInDBSerializer)
async def create_user_role(
    role_in: UserRoleCreateSerializer,
    db: Session = Depends(get_db),
    _: Permissions = Depends(Permissions(UserRolePermissions.user_role_create)),
) -> Any:
    """Create user role"""
    # Assert specified user and role exist
    user_dao.get_not_none(
        db,
        id=role_in.user_id,
        load_options=[load_only(User.id)],
    )
    role_dao.get_not_none(db, id=role_in.role_id)

    return user_role_dao.get_or_create(db, obj_in=role_in)


@router.get("/user-role", response_model=List[UserRoleInDBSerializer])
async def read_user_roles(
    user_role_filter: UserRoleFilter = FilterDepends(UserRoleFilter),
    db: Session = Depends(get_db),
    _: Permissions = Depends(Permissions(UserRolePermissions.user_role_list)),
) -> Any:
    """Read user roles"""
    user_role_filter_dict = user_role_filter.dict()

    if not any(
        user_role_filter_dict.values()
    ):  # Returns True if all values are falsy/None
        return user_role_dao.get_all(db)

    return user_role_dao.search(db, user_role_filter)


@router.patch(
    "/user-role/{user_role_id}",
    response_model=UserRoleInDBSerializer,
)
async def update_user_role(
    user_role_id: str,
    user_role_in: UserRoleUpdateSerializer,
    db: Session = Depends(get_db),
    _: Permissions = Depends(Permissions(UserRolePermissions.user_role_update)),
) -> Any:
    """Update User Role"""
    db_obj = user_role_dao.get_not_none(db, id=user_role_id)

    return user_role_dao.update(db, db_obj=db_obj, obj_in=user_role_in)


# Search query
# - Scope, create model country
# - Remove adminpermissions,
# - Create permissions
# - Assign users permissions
# Delete user role permissions
# Check everything works
# Admin create
# Nested filter in user role test
# Mapped columns
# Create scope under role after adding countries
# - Celery
# Redis
