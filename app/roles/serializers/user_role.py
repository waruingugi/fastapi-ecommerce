from app.db.serializer import InDBBaseSerializer
from pydantic import BaseModel, validator
from typing import List
from app.roles.constants import UserScopeTypes
from app.core.helpers import validate_phone_number


class UserRoleBaseSerializer(BaseModel):
    name: str
    scope: UserScopeTypes | None


class UserRoleInDBSerializer(InDBBaseSerializer, UserRoleBaseSerializer):
    permissions: List[str] | None


class UserRoleUpdateSerializer(UserRoleBaseSerializer):
    phone: str

    _validate_phone_number = validator("phone", pre=True, allow_reuse=True)(
        validate_phone_number
    )
