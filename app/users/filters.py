from pydantic import BaseModel
from app.users.constants import UserTypes


class UserFilter(BaseModel):
    is_active: bool | None
    user_types: UserTypes | None
