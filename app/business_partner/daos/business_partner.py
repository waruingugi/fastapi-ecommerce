from sqlalchemy.orm import Session
from app.db.dao import CRUDDao
from app.business_partner.models import BusinessPartner
from app.business_partner.serializers.business_partner import (
    BusinessPartnerCreateExistingOwnerSerializer,
    BusinessPartnerUpdateSerializer,
)
from typing import Optional


class BusinessPartnerDao(
    CRUDDao[
        BusinessPartner,
        BusinessPartnerCreateExistingOwnerSerializer,
        BusinessPartnerUpdateSerializer,
    ]
):
    def get_by_phone(self, db: Session, phone: str) -> Optional[BusinessPartner]:
        """Get a business partner by phone"""
        return self.get(db, phone=phone)

    def get_or_create(
        self,
        db: Session,
        obj_in: BusinessPartnerCreateExistingOwnerSerializer,
    ) -> BusinessPartner:
        """Get a business by phone if they exist, otherwise create"""
        business_partner_obj = self.get_by_phone(db, phone=obj_in.phone)

        if not business_partner_obj:
            business_partner_obj = self.create(db, obj_in=obj_in)

        return business_partner_obj


business_partner_dao = BusinessPartnerDao(BusinessPartner)
