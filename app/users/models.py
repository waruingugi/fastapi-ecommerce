from sqlalchemy import Column, Integer, String, Boolean, Index, DateTime
from sqlalchemy.orm import Mapped, relationship
from app.db.base_class import Base, get_current_datetime
from app.users.constants import UserTypes
from enum import Enum
from app.core.security import get_password_hash
from app.business_partner.models import BusinessPartner


class User(Base):
    date_joined = Column(DateTime, default=get_current_datetime)
    first_name: str = Column(String, nullable=True)
    last_name: str = Column(String, nullable=True)
    phone: Mapped[str] = Column(String, nullable=False, index=True)
    email: str = Column(String, unique=True, index=True, nullable=True)
    is_active = Column(Boolean, default=False)
    user_type = Column(
        String, default=UserTypes.CUSTOMER.value
    )
    hashed_password: str = Column(String, nullable=False)
    business_memberships = relationship("BusinessPartner", back_populates="owner", uselist=True)

    @property
    def get_username(self):
        if self.phone is None:
            return self.email
        else:
            return self.phone
