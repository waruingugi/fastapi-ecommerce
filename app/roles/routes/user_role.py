from app.core import deps
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.roles.serializers.user_role import UserRoleUpdateSerializer
from app.users.models import User
from app.roles.constants import UserPermissions
from typing import List
from app.users.daos.user import user_dao
from app.exceptions.custom import UserDoesNotExist


router = APIRouter()


@router.patch("/")
async def update_user_role(
    role_in: UserRoleUpdateSerializer,
    db: Session = Depends(deps.get_db),
    _: User = Depends(deps.get_current_active_superuser)
):
    user_in = user_dao.get_by_username(
        db, username=role_in.phone
    )

    if not user_in:
        raise UserDoesNotExist

    assign_perms = []
    for perm in UserPermissions:
        if role_in.name == perm.name:
            assign_perms.append(perm.value)

    return {"permission": assign_perms}

# Modify base permission to return list of perms
# In route, check if perm is in defined roles
# Assign user those roles
# Create in db
