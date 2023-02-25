from sqlalchemy.orm import Session
from app.db.dao import CRUDDao
from app.roles.serializers.user_role import (
    UserRoleUpdateSerializer,
    UserRoleCreateSerializer
)
from app.roles.models import UserRole
from app.roles.constants import UserPermissions
from app.users.daos.user import user_dao
from app.exceptions.custom import UserDoesNotExist


class UserRoleDao(
    CRUDDao[UserRole, UserRoleCreateSerializer, UserRoleUpdateSerializer]
):
    def on_pre_update(
        self, db: Session, db_obj: UserRole, values: dict, orig_values: dict
    ) -> None:
        """Automatically assign permissions based on role."""
        if orig_values.get("permissions", None):
            assign_perms = []
            role_name = orig_values.get("name", None)

            for perm in UserPermissions:
                if role_name == perm.name:
                    assign_perms.append(perm.value)

            # Convert permissions to string and save to model
            values["_permissions"] = ', '.join(map(str, assign_perms))

    
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
