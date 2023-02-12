from sqlalchemy.orm import Session
from app.db.dao import CRUDDao
from app.business_partner.models import Business
from app.business_partner.serializers.business_partner import (
    BusinessPartnerCreateSerializer,
    BusinessPartnerUpdateSerializer
)

class BusinessDao(CRUDDao[Business, BusinessPartnerCreateSerializer, BusinessPartnerUpdateSerializer]):
    pass


business_partner_dao = BusinessDao(Business)
