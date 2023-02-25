from app.db.base_class import Base
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from typing import List


class UserRole(Base):
    name = Column(String, nullable=False)
    _permissions = Column("permissions", Text())
    scope = Column(String, nullable=True)
    user_id = Column(String, ForeignKey("user.id"), unique=True)

    user = relationship("User", uselist=False)

    @property
    def permissions(self) -> List[str]:
        if self.permissions:
            return self._permissions.replace(" ", "").split(",")
        return []