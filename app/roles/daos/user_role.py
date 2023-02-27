from sqlalchemy.orm import Session
from app.db.dao import CRUDDao
from app.roles.serializers.user_role import (
    UserRoleUpdateSerializer,
    UserRoleCreateSerializer
)
from app.roles.models import UserRole
from app.roles.constants import UserRolePermissions
from app.users.daos.user import user_dao
from app.exceptions.custom import UserDoesNotExist


class UserRoleDao(
    CRUDDao[UserRole, UserRoleCreateSerializer, UserRoleUpdateSerializer]
):
    def get_permissions_from_role(self, role_name: str, permissions: str | None) -> str:
        """Generate permissions from role"""
        assign_perms = []
        if not permissions:
            for perm in UserRolePermissions:
                if role_name == perm.name:
                    assign_perms.extend(perm.value)  # Use extend to individually add list values to list

        # Return permissions as string
        # Use set() to ensure only unique string values are returned
        return (
            ', '.join(map(str, set(assign_perms))) if assign_perms else ''
        )

    def on_pre_create(self, db: Session, id: str, values: dict, orig_values: dict) -> None:
        values["permissions"] = self.get_permissions_from_role(
            orig_values["name"],
            orig_values.get("permissions", None)
        )

    def on_pre_update(
        self, db: Session, db_obj: UserRole, values: dict, orig_values: dict
    ) -> None:
        """Automatically assign permissions based on role."""
        values["permissions"] = self.get_permissions_from_role(
            orig_values["name"],
            orig_values.get("permissions", None)
        )

    def get_or_create(
        self, db: Session, obj_in: UserRoleUpdateSerializer,
    ) -> UserRole:
        """Get a role if it exists, otherwise create"""
        user = user_dao.get_by_username(
            db, username=obj_in.username
        )
        if not user:
            raise UserDoesNotExist

        user_role_obj = self.get(db, user_id=user.id)

        if not user_role_obj:
            new_user_role_obj = UserRoleCreateSerializer(
                user_id=user.id,
                name=obj_in.name,
                scope=obj_in.scope
            )
            user_role_obj = self.create(db, obj_in=new_user_role_obj)

        return user_role_obj

user_role_dao = UserRoleDao(UserRole)
