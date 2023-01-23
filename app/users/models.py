from sqlalchemy import Column, Integer, String, Boolean, Index, DateTime
from sqlalchemy.orm import Mapped, relationship
from app.db.base_class import Base, get_current_datetime
from app.users.constants import UserTypes
from enum import Enum
from typing import List


class User(Base):
    first_name: str = Column(String, nullable=False)
    last_name: str = Column(String, nullable=False)
    phone: Mapped[str] = Column(String, nullable=False, index=True)
    email: str = Column(String, unique=True, index=True, nullable=False)
    password: str = Column(String, nullbale=False)
    is_active: bool = Column(Boolean, default=False)
    user_type: str = Column(
        Enum(UserTypes),
        default=UserTypes.CUSTOMER.value
    )
    date_joined = Column(DateTime, default=get_current_datetime)
    business_memberships = relationship("Business", back_populates="owner", uselist=True)
