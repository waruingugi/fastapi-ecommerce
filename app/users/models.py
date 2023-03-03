from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, relationship
from app.db.base_class import Base, get_current_datetime
from app.users.constants import UserTypes


class User(Base):
    date_joined = Column(DateTime, default=get_current_datetime)
    first_name: str = Column(String, nullable=True)
    last_name: str = Column(String, nullable=True)
    phone: Mapped[str] = Column(String, nullable=False, index=True)
    email: str = Column(String, unique=True, index=True, nullable=True)
    is_active = Column(Boolean, default=False)
    user_type = Column(String, default=UserTypes.CUSTOMER.value)
    hashed_password: str = Column(String, nullable=False)

    business_memberships = relationship(
        "BusinessPartner", back_populates="owner", uselist=True
    )

    @property
    def get_username(self) -> str:
        return self.phone if self.phone else self.email
