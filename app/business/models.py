from sqlalchemy import Column, ForeignKey, String, Boolean, Index, DateTime
from sqlalchemy.orm import Mapped, relationship
from app.db.base_class import Base
from app.business.constants import BusinessTypes, BusinessVerificationStates
from enum import Enum


class Business(Base):
    name: str = Column(String, nullable=False)
    business_type: str = Column(
        String, default=BusinessTypes.SHOP.value,
    )
    email: str = Column(String, nullable=True)
    phone: Mapped[str] = Column(String, unique=True, nullable=False, index=True)
    is_verified = Column(Boolean, default=False)
    is_physical = Column(Boolean, default=False)
    verification_state = Column(
        String, default=BusinessVerificationStates.PENDING.value,
    )
    deleted = Column(Boolean, default=False)
    owner_id = Column(String, ForeignKey("user.id"), nullable=False)
    owner = relationship("User", back_populates="business_memberships")
    # accepted_payment_methods:
    # location:
    # country
    # currency
