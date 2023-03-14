from pydantic import BaseModel, validator
from app.db.serializer import InDBBaseSerializer
from app.commons.serializers.currency import CurrencyReadSerializer
from app.exceptions.custom import CustomHttpException


class CountryBaseSerializer(BaseModel):
    dialing_code: str
    name: str
    iso2_code: str
    iso3_code: str

    @validator("name", pre=True)
    def is_valid_name(cls, value) -> str:
        """Convert string to title"""
        return value.title()

    @validator("iso2_code", pre=True)
    def is_valid_iso2_code(cls, value) -> str:
        """Check iso2_code length"""
        if len(value) > 2:
            raise CustomHttpException(f"Invalid iso2_code {value}")
        return value.upper()

    @validator("iso3_code", pre=True)
    def is_valid_iso3_code(cls, value) -> str:
        """Check iso3_code length"""
        if not len(value) == 3:
            raise CustomHttpException(f"Invalid iso3_code {value}")
        return value.upper()


class CountryInDBSerializer(InDBBaseSerializer, CountryBaseSerializer):
    currency: CurrencyReadSerializer


class CountryCreateSerializer(CountryBaseSerializer):
    currency_id: str


class CountryReadSerializer(InDBBaseSerializer, CountryBaseSerializer):
    ...


class CountryUpdateSerializer(CountryBaseSerializer):
    dialing_code: str | None
    name: str | None
    iso2_code: str | None
    iso3_code: str | None
    currency_id: str | None
