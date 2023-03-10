from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import mapped_column
from app.db.base_class import Base, get_current_datetime
from app.users.constants import UserTypes


class User(Base):
    date_joined = mapped_column(DateTime, default=get_current_datetime)
    first_name = mapped_column(String, nullable=True)
    last_name = mapped_column(String, nullable=True)
    phone = mapped_column(String, nullable=False, index=True)
    email = mapped_column(String, unique=True, index=True, nullable=True)
    is_active = mapped_column(Boolean, default=False)
    user_type = mapped_column(String, default=UserTypes.CUSTOMER.value)
    hashed_password = mapped_column(String, nullable=False)

    @property
    def get_username(self) -> str:
        return self.phone if self.phone else self.email
