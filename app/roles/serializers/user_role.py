from app.db.serializer import InDBBaseSerializer
from pydantic import BaseModel, validator
from typing import List
from app.roles.constants import UserScopeTypes
from app.exceptions.custom import InvalidUserScopeType


class UserRoleBaseSerializer(BaseModel):
    name: str
    scope: str | None

    @validator('scope', pre=True)
    def is_valid_scope(cls, value) -> str | InvalidUserScopeType:
        """Validate scope is a valid UserScopeTypes object"""
        for scope in UserScopeTypes:
            if scope.value == value:
                return value

        return InvalidUserScopeType(f"{value} scope does not exist")


class UserRoleInDBSerializer(InDBBaseSerializer, UserRoleBaseSerializer):
    permissions: List[str] | None


class UserRoleCreateSerializer(UserRoleBaseSerializer):
    user_id: str


class UserRoleUpdateSerializer(UserRoleBaseSerializer):
    username: str
    scope: str
