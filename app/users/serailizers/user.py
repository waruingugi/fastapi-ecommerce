from pydantic import BaseModel, EmailStr, validator
from app.users.constants import UserTypes
from enum import Enum
from app.core.helpers import capitalize_fields, validate_phone_number
from datetime import datetime

class UserBaseSerializer(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str
    email: EmailStr
    is_active: bool | None = False


class UserCreateSerializer(UserBaseSerializer):
    user_type: str = UserTypes.CUSTOMER.value
    password: str | None = None

    _capitalize_fields = validator("first_name", "last_name", pre=True, allow_reuse=True)(
        capitalize_fields
    )

    _validate_phone_number = validator("phone", pre=True, allow_reuse=True)(
        validate_phone_number
    )


class UserActivateSerializer(UserCreateSerializer):
    is_active: bool = True


class UserUpdateSerializer(UserBaseSerializer):
    password: str | None = None


class UserInDBSerializer(UserBaseSerializer):
    id: str
    password: str
    user_type: str
