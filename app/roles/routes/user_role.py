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
    db: Session = Depends(deps.get_db),
    user_role_in: UserRoleCreateSerializer,
    _: User = Depends(deps.get_current_active_superuser)
):
    perm_classes: List[BasePermission] = []
    if user_role_in.permissions:
        for perm_in in user_role_in.permissions:
            pass

    return {"permission": "work in progress"}
