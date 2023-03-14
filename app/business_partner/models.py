from sqlalchemy import ForeignKey, String, Boolean
from sqlalchemy.orm import relationship, mapped_column
from app.db.base_class import Base
from app.business_partner.constants import (
    BusinessPartnerTypes,
    BusinessPartnerVerificationStates,
)


class BusinessPartner(Base):
    name = mapped_column(String, nullable=False)
    business_type = mapped_column(
        String,
        default=BusinessPartnerTypes.SHOP.value,
    )
    email = mapped_column(String, nullable=True)
    phone = mapped_column(String, unique=True, nullable=False, index=True)
    is_verified = mapped_column(Boolean, default=False)
    is_physical = mapped_column(Boolean, default=False)
    verification_state = mapped_column(
        String,
        default=BusinessPartnerVerificationStates.PENDING.value,
    )
    owner_id = mapped_column(String, ForeignKey("user.id"), nullable=False)
    owner = relationship("User", backref="business_memberships")

    @property
    def contact(self):
        if self.phone is not None:
            return self.phone
        else:
            return self.email

    @property
    def country(self):
        return self.owner.country.name
