from fastapi_sqlalchemy_filter import Filter
from app.commons.models import Currency, Country


class CurrencyFilter(Filter):
    name: str | None
    code: str | None

    class Constants(Filter.Constants):
        model = Currency


class CountryFilter(Filter):
    dialing_code: str | None
    name: str | None
    iso2_code: str | None
    iso3_code: str | None

    class Constants(Filter.Constants):
        model = Country
