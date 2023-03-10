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
