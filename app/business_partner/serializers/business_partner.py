from app.business_partner.constants import BusinessPartnerTypes
from app.db.serializer import InDBBaseSerializer
from app.users.serializers.user import (
    UserCreateSerializer,
    UserReadSerializer,
    BusinessPartnerBaseSerializer,
)
from app.core.helpers import _validate_bp_verification_state


class BusinessPartnerCreateSerializer(BusinessPartnerBaseSerializer):
    name: str
    business_type: str = BusinessPartnerTypes.SHOP.value
    owner: UserCreateSerializer


class BusinessPartnerCreateExistingOwnerSerializer(BusinessPartnerBaseSerializer):
    name: str
    business_type: str = BusinessPartnerTypes.SHOP.value
    owner_id: str


class BusinessPartnerUpdateSerializer(BusinessPartnerBaseSerializer):
    phone: str | None
    verification_state: str | None
    owner_id: str | None

    _validate_bp_verification_state = _validate_bp_verification_state


class BusinessPartnerInDBSerializer(InDBBaseSerializer, BusinessPartnerBaseSerializer):
    is_verified: str
    is_physical: bool
    verification_state: str
    owner: UserReadSerializer | None  # Remove None
