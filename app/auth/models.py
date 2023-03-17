from datetime import datetime
from app.db.base_class import Base
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    String,
)
from sqlalchemy.orm import relationship, mapped_column, column_property


class AuthToken(Base):
    access_token = mapped_column(String, nullable=False)
    refresh_token = mapped_column(String, nullable=True)
    user_id = mapped_column(String, ForeignKey("user.id", ondelete="CASCADE"))
    token_type = mapped_column(String, nullable=False)
    is_active = mapped_column(Boolean, nullable=False, default=True)
    access_token_eat = mapped_column(DateTime, nullable=False)
    refresh_token_eat = mapped_column(DateTime, nullable=False)

    refresh_token_is_valid = column_property(
        (is_active and datetime.utcnow() < refresh_token_eat)
    )

    user = relationship("User", uselist=False)
