from app.roles.daos.user_role import user_role_dao
from app.users.daos.user import user_dao
from app.roles.serializers.user_role import UserRoleUpdateSerializer
from app.users.constants import UserTypes
from app.roles.constants import UserScopeTypes
from app.db.session import SessionLocal

from sqlalchemy.orm import Session

def pre_migrate() -> None:
    pass


def post_migrate() -> None:
    """Populate UserRole model with data if it's empty"""
    with SessionLocal() as db:
        all_users = user_dao.get_all(db)

        for user in all_users:
            username = user.get_username
            user_role = UserRoleUpdateSerializer(
                username=username,
                name=UserTypes.CUSTOMER.value,
                scope=UserScopeTypes.COUNTRY.value,
            )
            user_role_dao.get_or_create(db, obj_in=user_role)
