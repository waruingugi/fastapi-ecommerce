from sqlalchemy import Column, ForeignKey, String, Boolean, Index, DateTime
from sqlalchemy.orm import Mapped, relationship
from app.db.base_class import Base
from business.constants import BusinessTypes, BusinessVerificationStates
from enum import Enum


class Business(Base):
    name: str = Column(String, nullable=False)
    business_type: str = Column(
        Enum(BusinessTypes),
        default=BusinessTypes.SHOP.value,
    )
    email: str = Column(String, nullable=True)
    phone: Mapped[str] = Column(String, unique=True, nullable=False, index=True)
    is_verified: bool = Column(Boolean, default=False, server_default=False())
    is_physical: bool = Column(Boolean, default=False, server_default=False())
    verification_state: str = Column(
        Enum(BusinessVerificationStates),
        default=BusinessVerificationStates.PENDING.value,
    )
    deleted = Column(Boolean, default=False, server_default=False())
    owner_id: str = Column(String, ForeignKey("user.id"), nullable=False)
    owner = relationship("User", back_populates="business_memberships")
    # accepted_payment_methods:
    # location:
    # country
    # currency
