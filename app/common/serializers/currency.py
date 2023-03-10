from pydantic import BaseModel
from app.db.serializer import InDBBaseSerializer


class CurrencyBaseSerializer(BaseModel):
    name: str | None
    code: str | None


class CurrencyInDBSerializer(InDBBaseSerializer, CurrencyBaseSerializer):
    ...


class CurrencyCreateSerializer(CurrencyBaseSerializer):
    ...


class CurrencyReadSerializer(CurrencyBaseSerializer):
    ...


class CurrencyUpdateSerializer(CurrencyBaseSerializer):
    ...
