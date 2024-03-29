from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped
from typing import Dict
from sqlalchemy_utils import get_columns
from sqlalchemy.orm import mapped_column

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
    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    created_at = mapped_column(DateTime, default=get_current_datetime, nullable=False)
    updated_at = mapped_column(
        DateTime, default=None, onupdate=get_current_datetime, nullable=True
    )

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def get_model_columns(cls) -> Dict[str, str]:
        return get_columns(cls).keys()
