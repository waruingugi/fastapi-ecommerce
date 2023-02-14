from pydantic import BaseModel, EmailStr, validator
from app.users.constants import UserTypes
from app.core.helpers import (
    capitalize_fields,
    validate_phone_number,
    validate_email
)
from app.db.serializer import InDBBaseSerializer
from datetime import datetime
from app.db.base_class import generate_uuid
from typing import List, Optional


class BusinessPartnerBaseSerializer(BaseModel):
    name: str | None
    email: EmailStr | None
    phone: str
    is_physical: bool = False

    _capitalize_fields = validator("name", pre=True, allow_reuse=True)(
        capitalize_fields
    )

    _validate_phone_number = validator("phone", pre=True, allow_reuse=True)(
        validate_phone_number
    )

    _validate_email = validator("email", pre=True, allow_reuse=True)(
        validate_email
    )


class BusinessParnterReadSerializer(BusinessPartnerBaseSerializer, InDBBaseSerializer):
    pass


class UserBaseSerializer(BaseModel):
    first_name: str | None
    last_name: str | None
    phone: str | None
    email: EmailStr | None

    _capitalize_fields = validator("first_name", "last_name", pre=True, allow_reuse=True)(
        capitalize_fields
    )

    _validate_phone_number = validator("phone", pre=True, allow_reuse=True)(
        validate_phone_number
    )

    _validate_email = validator("email", pre=True, allow_reuse=True)(
        validate_email
    )


class UserCreateSerializer(UserBaseSerializer):
    phone: str
    password: str | None

    @validator('password', pre=True, always=True)
    def set_ts_now(cls, value):
        return value or generate_uuid()


class UserActivateDeactivateSerializer(BaseModel):
    is_active: bool


class UserUpdateSerializer(UserBaseSerializer):
    user_type: str | None
    password: str | None


class UserInDBSerializer(InDBBaseSerializer, UserBaseSerializer):
    user_type: str
    date_joined: datetime
    business_memberships: Optional[List[BusinessParnterReadSerializer]]


class UserReadSerializer(UserBaseSerializer, InDBBaseSerializer):
    pass
