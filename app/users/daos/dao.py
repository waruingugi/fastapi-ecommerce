from app.db.dao import CRUDBase
from app.users.models import User
from app.users.serailizers.user import UserCreateSerializer, UserUpdateSerializer


class UserDao(CRUDBase[User, UserCreateSerializer, UserUpdateSerializer]):
    ...


user_dao = UserDao(User)
