from sqlalchemy.orm import Session
from app.db.dao import CRUDDao
from app.roles.serializers.user_role import (
    UserRoleUpdateSerializer,
    UserRoleCreateSerializer,
)
from app.roles.models import UserRole
from app.core.helpers import convert_list_to_string


class UserRoleDao(
    CRUDDao[UserRole, UserRoleCreateSerializer, UserRoleUpdateSerializer]
):
    def on_pre_create(
        self, db: Session, id: str, values: dict, orig_values: dict
    ) -> None:
        values["scope"] = convert_list_to_string(orig_values.get("scope", []))

    def on_pre_update(
        self, db: Session, db_obj: UserRole, values: dict, orig_values: dict
    ) -> None:
        values["scope"] = convert_list_to_string(orig_values.get("scope", []))

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
