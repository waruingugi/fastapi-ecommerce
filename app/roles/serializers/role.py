from app.db.serializer import InDBBaseSerializer
from pydantic import BaseModel, validator
from typing import List
from app.users.constants import UserTypes
from app.exceptions.custom import CustomHttpException
from app.auth.permissions import AllAppPermissions


class RoleBaseSerializer(BaseModel):
    name: str
    permissions: List[str]

    @validator("name", pre=True)
    def is_valid_name(cls, value) -> str:
        """Validate role name is a valid UserType object"""
        value = value.upper()  # Convert to UPPERCASE
        if value not in UserTypes.list_():
            raise CustomHttpException(f"The role name {value} does not exist")

        return value

    @validator("permissions", pre=True)
    def is_valid_permissions(cls, value) -> List[str]:
        """Validate permissions are valid"""
        for permission in value:
            if permission not in AllAppPermissions:
                raise CustomHttpException(f"The permission {permission} does not exist")

        return value


class RoleInDBSerializer(InDBBaseSerializer, RoleBaseSerializer):
    ...


class RoleCreateSerializer(RoleBaseSerializer):
    ...


class RoleUpdateSerializer(RoleBaseSerializer):
    name: str | None
    permissions: List[str] | None
