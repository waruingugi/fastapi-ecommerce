from datetime import datetime
from app.db.base_class import Base
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from typing import List


class AuthToken(Base):
    access_token: str = Column(String, nullable=False)
    refresh_token = Column(String, nullable=True)
    user_id = Column(String, ForeignKey("user.id"))
    token_type: str = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    access_token_eat: datetime = Column(DateTime, nullable=False)
    refresh_token_eat: datetime = Column(DateTime, nullable=False)

    user = relationship("User", uselist=False)

    @property
    def refresh_token_is_valid(self) -> bool:
        return bool(self.is_active) and (datetime.utcnow() < self.refresh_token_eat)


class UserRole(Base):
    name = Column(String, nullable=False)
    _permissions = Column(Text())
    scope = Column(String, nullable=True)
    user_id = Column(String, ForeignKey("user.id"), unique=True)

    user = relationship("User", uselist=False)

    @property
    def permissions(self) -> List[str]:
        if self.permissions:
            return self._permissions.replace(" ", "").split(",")
        return []
