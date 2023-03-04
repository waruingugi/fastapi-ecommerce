from app.users.constants import UserTypes
from fastapi_sqlalchemy_filter import Filter
from app.users.models import User


class UserFilter(Filter):
    contact: str | None
    is_active: bool | None
    user_type: UserTypes | None

    class Constants(Filter.Constants):
        model = User
        search_field_name = "contact"
        search_model_fields = ["phone", "email"]
