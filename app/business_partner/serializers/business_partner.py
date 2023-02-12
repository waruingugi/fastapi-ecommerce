from pydantic import BaseModel, EmailStr
from app.business_partner.constants import BusinessTypes
from app.db.serializer import InDBBaseSerializer


class BusinessPartnerBaseSerializer(BaseModel):
    name: str | None
    email: EmailStr | None
    phone: str | None
    is_verified: bool = False
    is_physical: bool = False


class BusinessPartnerCreateSerializer(BusinessPartnerBaseSerializer):
    name: str
    phone: str
    business_type: str = BusinessTypes.SHOP.value


class BusinessPartnerUpdateSerializer(BusinessPartnerBaseSerializer):
    is_verified: bool | None
    is_physical: bool | None
    verification_state: str | None
    deleted: bool | None


class BusinessPartnerInDBSerializer(InDBBaseSerializer, BusinessPartnerBaseSerializer):
    is_verified: str
    is_physical: bool
    verification_state: str
    deleted: bool
