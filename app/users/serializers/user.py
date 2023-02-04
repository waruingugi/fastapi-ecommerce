from pydantic import BaseModel, EmailStr, validator
from app.users.constants import UserTypes
from app.core.helpers import capitalize_fields, validate_phone_number
from app.db.serializer import InDBBaseSerializer
from datetime import datetime


class UserBaseSerializer(BaseModel):
    first_name: str | None
    last_name: str | None
    phone: str | None
    email: EmailStr | None
    is_active: bool = False


class UserCreateSerializer(UserBaseSerializer):
    phone: str
    user_type: str = UserTypes.CUSTOMER.value
    password: str

    _capitalize_fields = validator("first_name", "last_name", pre=True, allow_reuse=True)(
        capitalize_fields
    )

    _validate_phone_number = validator("phone", pre=True, allow_reuse=True)(
        validate_phone_number
    )


class UserActivateDeactivateSerializer(UserBaseSerializer):
    is_active: bool


class UserUpdateSerializer(UserBaseSerializer):
    user_type: str | None
    password: str | None


class UserInDBSerializer(InDBBaseSerializer, UserBaseSerializer):
    user_type: str
    date_joined: datetime

    class Config:
        orm_mode = True
