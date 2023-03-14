from app.db.serializer import InDBBaseSerializer
from pydantic import BaseModel, validator
from app.users.serializers.user import UserReadSerializer
from typing import Sequence
from app.exceptions.custom import CustomHttpException


class UserRoleBaseSerializer(BaseModel):
    user_id: str
    role_id: str
    scope: Sequence[str] | None

    @validator("scope", pre=True)
    def validate_scope(cls, value) -> str:
        """Assert scope is valid iso3_code length and is capitals"""
        for scope in value:
            if (not scope.isupper()) or (not len(scope) == 2):
                raise CustomHttpException(f"Invalid scope {value}")
        return value


class UserRoleInDBSerializer(InDBBaseSerializer, UserRoleBaseSerializer):
    user: UserReadSerializer


class UserRoleCreateSerializer(UserRoleBaseSerializer):
    ...


class UserRoleUpdateSerializer(UserRoleBaseSerializer):
    user_id: str | None
    role_id: str | None
