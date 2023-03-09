from fastapi_sqlalchemy_filter import Filter, FilterDepends, with_prefix
from app.roles.models import UserRole, Role
from app.users.constants import UserTypes


class RoleFilter(Filter):
    name: UserTypes | None

    class Constants(Filter.Constants):
        model = Role


class UserRoleFilter(Filter):
    role: RoleFilter | None = FilterDepends(with_prefix("role", RoleFilter))

    class Constants(Filter.Constants):
        model = UserRole
