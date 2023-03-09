from app.core.deps import get_db, Permissions, get_current_active_superuser
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.roles.serializers.role import (
    RoleUpdateSerializer,
    RoleCreateSerializer,
    RoleInDBSerializer,
)
from typing import List
from app.roles.daos.role import role_dao
from app.core.logger import LoggingRoute
from app.roles.filters import RoleFilter
from app.roles.permissions import RolePermissions
from fastapi_sqlalchemy_filter import FilterDepends
from typing import Any
from app.users.models import User

router = APIRouter(route_class=LoggingRoute)


@router.post("/", response_model=RoleInDBSerializer)
async def create_role(
    role_in: RoleCreateSerializer,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_superuser),
) -> Any:
    """Create user role"""
    return role_dao.get_or_create(db, obj_in=role_in)


@router.get("/", response_model=List[RoleInDBSerializer])
async def read_roles(
    role_filter: RoleFilter = FilterDepends(RoleFilter),
    db: Session = Depends(get_db),
    _: Permissions = Depends(Permissions(RolePermissions.role_list)),
) -> Any:
    """Read user roles"""
    role_filter_dict = role_filter.dict()

    if not any(role_filter_dict.values()):  # Returns True if all values are falsy/None
        return role_dao.get_all(db)

    return role_dao.search(db, role_filter)


@router.patch("/{role_id}", response_model=RoleInDBSerializer)
async def update_role(
    role_id: str,
    role_in: RoleUpdateSerializer,
    db: Session = Depends(get_db),
    _: Permissions = Depends(Permissions(RolePermissions.role_update)),
) -> Any:
    """Update role"""
    # Get the business_partner to be updated
    db_obj = role_dao.get(db, id=role_id)

    return role_dao.update(db, db_obj=db_obj, obj_in=role_in)
