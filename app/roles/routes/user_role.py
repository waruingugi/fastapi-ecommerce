from app.core import deps
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.roles.serializers.user_role import (
    UserRoleUpdateSerializer,
    UserRoleInDBSerializer,
    UserRoleInDBSerializer
)
from app.users.models import User
from typing import List
from app.users.daos.user import user_dao
from app.exceptions.custom import UserDoesNotExist
from app.roles.daos.user_role import user_role_dao
from app.roles.permissions import UserRolePermissions
from app.core.logger import LoggingRoute

router = APIRouter(route_class=LoggingRoute)


@router.post("/", response_model=UserRoleInDBSerializer)
async def create_user_role(
    role_in: UserRoleUpdateSerializer,
    db: Session = Depends(deps.get_db),
    _: User = Depends(deps.get_current_active_superuser)
):
    """Create user role"""
    return user_role_dao.get_or_create(db, obj_in=role_in)


@router.get("/roles", response_model=List[UserRoleInDBSerializer])
async def read_user_roles(
    db: Session = Depends(deps.get_db),
    _: User = Depends(deps.get_current_active_superuser),
    permissions: deps.Permissions = Depends(deps.Permissions(UserRolePermissions.user_role_list))
):
    """Read user roles"""
    return user_role_dao.get_all(db)


# Permissions: use in dependencies
# - Permissions class
# - Calls permission check func
# - In check func
# - search user_id in permissions
# - Get permissions in role
# - Check role has specified in permissions
# Customer
# Violates foreign key constraint

# Logger
# Permissions: put roles in token
# Black and coding
# Search query
# TSVector