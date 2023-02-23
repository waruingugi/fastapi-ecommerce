from app.db.serializer import InDBBaseSerializer
from pydantic import BaseModel
from typing import List
from app.roles.constants import UserScopeTypes


class UserRoleBaseSerializer(BaseModel):
    name: str
    scope: UserScopeTypes | None


class UserRoleInDBSerializer(InDBBaseSerializer, UserRoleBaseSerializer):
    permissions: List[str] | None


class UserRoleCreateSerializer(UserRoleBaseSerializer):
    pass
