from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import Mapped
from sqlalchemy import event
from typing import Optional, Callable

import uuid
from datetime import datetime

BaseClass = declarative_base()


def get_current_datetime() -> datetime:
    return datetime.now()


def generate_uuid() -> str:
    return str(uuid.uuid4())


class Base(BaseClass):
    __abstract__ = True
    __name__: str

    # All tables inheriting from Base class contains this columns
    id: Mapped[str] = Column(String, primary_key=True, default=generate_uuid)
    created_at: Mapped[datetime] = Column(
        DateTime, default=get_current_datetime, nullable=False
    )
    updated_at = Column(
        DateTime, default=None, onupdate=get_current_datetime, nullable=True
    )

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def on_pre_create(cls, mapper, connection, target) -> Optional[Callable]:
        """Execute before INSERT SQL statement"""
        if hasattr(target, 'on_pre_create'):
            target.on_pre_create()


# Register event listeners
event.listen(Base, 'before_insert', Base.on_pre_create, propagate=True)
