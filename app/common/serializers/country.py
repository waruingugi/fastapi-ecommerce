from pydantic import BaseModel, validator
from app.db.serializer import InDBBaseSerializer
from app.common.serializers.currency import CurrencyReadSerializer


class CountryBaseSerializer(BaseModel):
    dialing_code: str | None
    name: str | None
    iso2_code: str | None
    iso3_code: str | None

    @validator("name", pre=True)
    def is_valid_name(cls, value) -> str:
        """Convert string to title"""
        return value.title()


class CountryInDBSerializer(InDBBaseSerializer, CountryBaseSerializer):
    currency: CurrencyReadSerializer


class CountryCreateSerializer(CountryBaseSerializer):
    currency_id: str


class CountryReadSerializer(CountryBaseSerializer):
    ...


class CountryUpdateSerializer(CountryBaseSerializer):
    currency_id: str
