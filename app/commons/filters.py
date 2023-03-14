from fastapi_sqlalchemy_filter import Filter
from app.commons.models import Currency, Country
from pydantic import Field


class CurrencyFilter(Filter):
    name: str | None
    code: str | None

    class Constants(Filter.Constants):
        model = Currency


class CountryBaseFilter(Filter):
    class Constants(Filter.Constants):
        model = Country


class CountryFilter(CountryBaseFilter):
    name__ilike: str | None = Field(alias="country_name")
    iso3_code__ilike: str | None = Field(alias="iso3_code")


class CountryScopeFilter(CountryBaseFilter):
    iso2_code__in: list[str] | None
