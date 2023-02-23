# Route
# User role serializer
# Is superadmin

from app.core import deps
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from app.roles.serializers.user_role import UserRoleCreateSerializer
from app.users.models import User
from app.db.permissions import BasePermission
from typing import List


router = APIRouter()

@router.post("/")
async def create_user_role(
    user_role_in: UserRoleCreateSerializer,
    db: Session = Depends(deps.get_db),
    _: User = Depends(deps.get_current_active_superuser)
):

    return {"permission": "work in progress"}

# Modify base permission to return list of perms
# In route, check if perm is in defined roles
# Assign user those roles
# Create in db
