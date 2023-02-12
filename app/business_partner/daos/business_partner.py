from sqlalchemy.orm import Session
from app.db.dao import CRUDDao
from app.business_partner.models import Business
from app.business_partner.serializers.business_partner import (
    BusinessPartnerCreateSerializer,
    BusinessPartnerCreateExistingOwnerSerializer,
    BusinessPartnerUpdateSerializer
)
from typing import Optional, Union


class BusinessDao(
    CRUDDao[
        Business,
        Union[
            BusinessPartnerCreateSerializer,
            BusinessPartnerCreateExistingOwnerSerializer
        ],
        BusinessPartnerUpdateSerializer
    ]
):
    def get_by_phone(self, db: Session, phone: str) -> Optional[Business]:
        """Get a business partner by phone"""
        return self.get(db, phone=phone)
    
    def get_or_create(
        self, db: Session,
        obj_in: Union[
            BusinessPartnerCreateSerializer,
            BusinessPartnerCreateExistingOwnerSerializer
        ],
    ) -> Business:
        """Get a business by phone if they exist, otherwise create"""
        business_obj = self.get_by_phone(db, phone=obj_in.phone)

        if not business_obj:
            business_obj = self.create(db, obj_in=obj_in)

        return business_obj


business_partner_dao = BusinessDao(Business)
