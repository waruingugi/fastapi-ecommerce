from app.users.constants import UserTypes
from fastapi_sqlalchemy_filter import Filter, FilterDepends, with_prefix
from app.users.models import User
from typing import List
from app.commons.filters import CountryFilter


class UserBaseFilter(Filter):
    contact: str | None
    country: CountryFilter | None = FilterDepends(with_prefix("country", CountryFilter))

    class Constants(Filter.Constants):
        model = User
        search_field_name = "contact"
        search_model_fields = ["phone", "email"]


class UserFilter(UserBaseFilter):
    is_active: bool | None
    user_type: UserTypes | None
    order_by: List[str] | None
