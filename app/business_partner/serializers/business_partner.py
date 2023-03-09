from app.business_partner.constants import BusinessPartnerTypes
from app.db.serializer import InDBBaseSerializer
from app.users.serializers.user import (
    UserReadSerializer,
    BusinessPartnerBaseSerializer,
)
from app.core.helpers import _validate_bp_verification_state


class BusinessPartnerCreateExistingOwnerSerializer(BusinessPartnerBaseSerializer):
    name: str
    business_type: str | None = BusinessPartnerTypes.SHOP.value
    owner_id: str


class BusinessPartnerUpdateSerializer(BusinessPartnerBaseSerializer):
    phone: str | None
    verification_state: str | None
    owner_id: str | None

    _validate_bp_verification_state = _validate_bp_verification_state


class BusinessPartnerInDBSerializer(InDBBaseSerializer, BusinessPartnerBaseSerializer):
    business_type: str
    is_verified: str
    is_physical: bool
    verification_state: str
    owner: UserReadSerializer
