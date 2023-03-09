from app.db.base_class import Base
from sqlalchemy import (
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property
from typing import List


class Role(Base):
    name = mapped_column(String, nullable=False)
    _permissions = mapped_column("permissions", Text())

    @hybrid_property
    def permissions(self) -> List[str]:
        if self._permissions:
            return self._permissions.replace(" ", "").split(",")
        return []


class UserRole(Base):
    user_id = mapped_column(String, ForeignKey("user.id", ondelete="CASCADE"))
    role_id = mapped_column(String, ForeignKey("role.id", ondelete="CASCADE"))

    user = relationship("User", backref="user_role")


"""
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

class Role(Base):
    name = mapped_column(String, nullable=False)
    _permissions = mapped_column("permissions", Text())

    @hybrid_property
    def permissions(self) -> List[str]:
        if self._permissions:
            return self._permissions.replace(" ", "").split(",")
        return []


class UserRole(Base):
    user_id = mapped_column(String, ForeignKey("user.id", ondelete='CASCADE'), unique=True)
    role_id = mapped_column(String, ForeignKey("role.id", ondelete='PROTECT'), nullable=False)

    user = relationship("User", backref="user_role", uselist=False)

"""
