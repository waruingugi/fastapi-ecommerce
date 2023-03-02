from app.filters import Filter
from typing import Optional
from app.roles.models import UserRole


class UserRoleFilter(Filter):
    name: Optional[str]
    user_id: Optional[str]

    class Constants(Filter.Constants):
        model = UserRole
