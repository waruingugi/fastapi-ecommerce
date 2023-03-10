from fastapi_sqlalchemy_filter import Filter
from app.common.models import Currency


class CurrencyFilter(Filter):
    name: str | None
    code: str | None

    class Constants(Filter.Constants):
        model = Currency
