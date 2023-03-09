from sqlalchemy.orm import Session
from app.db.dao import CRUDDao
from app.roles.serializers.user_role import (
    UserRoleUpdateSerializer,
    UserRoleCreateSerializer,
)
from app.roles.models import UserRole


class UserRoleDao(
    CRUDDao[UserRole, UserRoleCreateSerializer, UserRoleUpdateSerializer]
):
    def get_or_create(
        self,
        db: Session,
        obj_in: UserRoleCreateSerializer,
    ) -> UserRole:
        """Get a role if it exists, otherwise create"""
        user_role = self.get(db, user_id=obj_in.user_id)

        if not user_role:
            user_role = self.create(db, obj_in=obj_in)

        return user_role


user_role_dao = UserRoleDao(UserRole)
