from pydantic import BaseModel, EmailStr, validator
from app.core.helpers import (
    capitalize_fields,
    _capitalize_fields,
    _validate_phone_number,
    _validate_email,
)
from app.db.serializer import InDBBaseSerializer
from app.commons.serializers.country import CountryReadSerializer
from datetime import datetime
from app.db.base_class import generate_uuid
from typing import List, Optional


class BusinessPartnerBaseSerializer(BaseModel):
    name: str | None
    email: EmailStr | None
    phone: str
    is_physical: bool | None = False

    _capitalize_fields = _capitalize_fields
    _validate_phone_number = _validate_phone_number
    _validate_email = _validate_email


class BusinessParnterReadSerializer(BusinessPartnerBaseSerializer, InDBBaseSerializer):
    pass


class UserBaseSerializer(BaseModel):
    first_name: str | None
    last_name: str | None
    phone: str | None
    email: EmailStr | None

    _validate_phone_number = _validate_phone_number
    _validate_email = _validate_email

    _capitalize_fields = validator(
        "first_name", "last_name", pre=True, allow_reuse=True
    )(capitalize_fields)


class UserCreateSerializer(UserBaseSerializer):
    phone: str
    password: str | None
    country_id: str

    @validator("password", pre=True, always=True)
    def generate_random_password(cls, value):
        return value or generate_uuid()


class UserUpdateSerializer(UserBaseSerializer):
    user_type: str | None
    is_active: bool | None
    password: str | None
    country_id: str | None


class UserInDBSerializer(InDBBaseSerializer, UserBaseSerializer):
    user_type: str
    date_joined: datetime
    is_active: bool
    country: CountryReadSerializer | None
    business_memberships: Optional[List[BusinessParnterReadSerializer]]


class UserReadSerializer(UserBaseSerializer, InDBBaseSerializer):
    pass
