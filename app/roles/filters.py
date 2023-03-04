from fastapi_sqlalchemy_filter import Filter
from app.roles.models import UserRole


class UserRoleFilter(Filter):
    name: str | None
    user_id: str | None

    class Constants(Filter.Constants):
        model = UserRole
