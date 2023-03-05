from app.users.constants import UserTypes
from fastapi_sqlalchemy_filter import Filter
from app.users.models import User
from typing import List


class UserBaseFilter(Filter):
    contact: str | None
    order_by: List[str] | None

    class Constants(Filter.Constants):
        model = User
        search_field_name = "contact"
        search_model_fields = ["phone", "email"]


class UserFilter(UserBaseFilter, Filter):
    is_active: bool | None
    user_type: UserTypes | None
