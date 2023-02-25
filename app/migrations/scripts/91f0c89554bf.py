from app.roles.daos.user_role import user_role_dao
from app.users.daos.user import user_dao

from sqlalchemy.orm import Session

def pre_migrate() -> None:
    pass


def post_migrate(db: Session) -> None:
    """Populate UserRole model with data if it's empty"""
    all_users = user_dao.get_all(db)

    for user in all_users:
        pass

    print("I'm alive!")
