from sqlalchemy import Column, ForeignKey, String, Boolean
from sqlalchemy.orm import Mapped, relationship
from app.db.base_class import Base
from app.business_partner.constants import (
    BusinessPartnerTypes,
    BusinessPartnerVerificationStates,
)


class BusinessPartner(Base):
    name: str = Column(String, nullable=False)
    business_type: str = Column(
        String,
        default=BusinessPartnerTypes.SHOP.value,
    )
    email: str = Column(String, nullable=True)
    phone: Mapped[str] = Column(String, unique=True, nullable=False, index=True)
    is_verified = Column(Boolean, default=False)
    is_physical = Column(Boolean, default=False)
    verification_state = Column(
        String,
        default=BusinessPartnerVerificationStates.PENDING.value,
    )
    deleted = Column(Boolean, default=False)
    owner_id = Column(String, ForeignKey("user.id"), nullable=False)
    owner = relationship("User", backref="business_memberships")
    # accepted_payment_methods:
    # location:
    # country
    # currency

    @property
    def contact(self):
        if self.phone is not None:
            return self.phone
        else:
            return self.email
