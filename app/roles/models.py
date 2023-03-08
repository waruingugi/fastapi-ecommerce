from app.db.base_class import Base
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import relationship, mapped_column
from typing import List


class UserRole(Base):
    name = Column(String, nullable=False)
    _permissions = Column("permissions", Text())
    scope = mapped_column(String, nullable=True)
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"), unique=True)

    user = relationship("User", uselist=False)

    @property
    def permissions(self) -> List[str]:
        if self._permissions:
            return self._permissions.replace(" ", "").split(",")
        return []


"""
class Role(Base):
    name = Column(String, nullable=False)
    _permissions = Column("permissions", Text())


class UserRole(Base):
    user_id = Column(String, ForeignKey("user.id", ondelete='CASCADE'), unique=True)
    role_id = Column(String, ForeignKey("role.id", ondelete='PROTECT'), nullable=False)

    user = relationship("User", uselist=False)

    @property
    def permissions(self) -> List[str]:
        if self._permissions:
            return self._permissions.replace(" ", "").split(",")
        return []
"""
