from pydantic import BaseModel, EmailStr, validator
from app.business_partner.constants import BusinessTypes
from app.db.serializer import InDBBaseSerializer
from app.users.serializers.user import UserReadSerializer
from app.core.helpers import (
    capitalize_fields,
    validate_phone_number,
    validate_email
)


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


class BusinessPartnerCreateSerializer(BusinessPartnerBaseSerializer):
    name: str
    business_type: str = BusinessTypes.SHOP.value
    owner: UserReadSerializer


class BusinessPartnerCreateExistingOwnerSerializer(BusinessPartnerBaseSerializer):
    name: str
    business_type: str = BusinessTypes.SHOP.value
    owner_id: str


class BusinessPartnerUpdateSerializer(BusinessPartnerBaseSerializer):
    verification_state: str | None
    deleted: bool | None


class BusinessPartnerInDBSerializer(InDBBaseSerializer, BusinessPartnerBaseSerializer):
    is_verified: str
    is_physical: bool
    verification_state: str

    class Config:
        orm_mode = True
