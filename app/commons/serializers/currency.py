from pydantic import BaseModel, validator
from app.db.serializer import InDBBaseSerializer


class CurrencyBaseSerializer(BaseModel):
    name: str | None
    code: str | None

    @validator("name", pre=True)
    def is_valid_name(cls, value) -> str:
        """Convert string to title"""
        return value.title()


class CurrencyInDBSerializer(InDBBaseSerializer, CurrencyBaseSerializer):
    ...


class CurrencyCreateSerializer(CurrencyBaseSerializer):
    ...


class CurrencyReadSerializer(InDBBaseSerializer, CurrencyBaseSerializer):
    ...


class CurrencyUpdateSerializer(CurrencyBaseSerializer):
    ...
