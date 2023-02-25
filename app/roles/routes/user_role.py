from app.core import deps
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.roles.serializers.user_role import (
    UserRoleUpdateSerializer,
    UserRoleInDBSerializer
)
from app.users.models import User
from app.roles.constants import UserPermissions
from typing import List
from app.users.daos.user import user_dao
from app.exceptions.custom import UserDoesNotExist
from app.roles.daos.user_role import user_role_dao


router = APIRouter()


@router.post("/", response_model=UserRoleInDBSerializer)
async def create_user_role(
    role_in: UserRoleUpdateSerializer,
    db: Session = Depends(deps.get_db),
    _: User = Depends(deps.get_current_active_superuser)
):
    """Update user role"""
    return user_role_dao.get_or_create(db, obj_in=role_in)

# Alembic create role
# On user create, create userrole