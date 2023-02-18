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


class AuthToken(Base):
    access_token: str = Column(String, nullable=False)
    refresh_token = Column(String, nullable=True)
    user_id = Column(String, ForeignKey("user.id"))
    token_type: str = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    access_token_expires_at: datetime = Column(DateTime, nullable=False)
    refresh_token_expires_at: datetime = Column(DateTime, nullable=False)

    user = relationship("User", uselist=False)

    @property
    def refresh_token_is_valid(self) -> bool:
        return bool(self.is_active) and (datetime.utcnow() < self.refresh_token_expires_at)

    @property
    def access_token_is_valid(self) -> bool:
        return bool(self.is_active) and (datetime.utcnow() < self.access_token_expires_at)
