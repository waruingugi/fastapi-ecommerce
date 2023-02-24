from sqlalchemy.orm import Session
from app.db.dao import CRUDDao
from app.roles.serializers.user_role import (
    UserRoleUpdateSerializer,
    UserRoleCreateSerializer
)
from app.roles.models import UserRole


class UserRolesDao(
    CRUDDao[UserRole, UserRoleCreateSerializer, UserRoleUpdateSerializer]
):
    def on_pre_update(
        self, db: Session, db_obj: UserRole, values: dict, orig_values: dict
    ) -> None:
        pass