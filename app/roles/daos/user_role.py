from sqlalchemy.orm import Session
from app.db.dao import CRUDDao
from app.roles.serializers.user_role import (
    UserRoleUpdateSerializer,
    UserRoleCreateSerializer
)
from app.roles.models import UserRole
from app.roles.constants import UserPermissions


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

user_role_dao = UserRoleDao(UserRole)
