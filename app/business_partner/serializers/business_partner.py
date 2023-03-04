from app.business_partner.constants import BusinessTypes
from app.db.serializer import InDBBaseSerializer
from app.users.serializers.user import (
    UserCreateSerializer,
    UserReadSerializer,
    BusinessPartnerBaseSerializer,
)


class BusinessPartnerCreateSerializer(BusinessPartnerBaseSerializer):
    name: str
    business_type: str = BusinessTypes.SHOP.value
    owner: UserCreateSerializer


class BusinessPartnerCreateExistingOwnerSerializer(BusinessPartnerBaseSerializer):
    name: str
    business_type: str = BusinessTypes.SHOP.value
    owner_id: str


class BusinessPartnerUpdateSerializer(BusinessPartnerBaseSerializer):
    verification_state: str | None
    owner_id: str | None


class BusinessPartnerInDBSerializer(InDBBaseSerializer, BusinessPartnerBaseSerializer):
    is_verified: str
    is_physical: bool
    verification_state: str
    owner: UserReadSerializer | None  # Remove None
