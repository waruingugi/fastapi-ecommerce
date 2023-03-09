from sqlalchemy.orm import Session
from app.db.dao import CRUDDao
from app.roles.serializers.role import (
    RoleUpdateSerializer,
    RoleCreateSerializer,
)
from app.roles.models import Role
from app.core.helpers import convert_perms_list_to_string


class RoleDao(CRUDDao[Role, RoleCreateSerializer, RoleUpdateSerializer]):
    def on_pre_create(
        self, db: Session, id: str, values: dict, orig_values: dict
    ) -> None:
        values["permissions"] = convert_perms_list_to_string(
            orig_values.get("permissions", [])
        )

    def on_pre_update(
        self, db: Session, db_obj: Role, values: dict, orig_values: dict
    ) -> None:
        values["permissions"] = convert_perms_list_to_string(
            orig_values.get("permissions", [])
        )

    def get_or_create(
        self,
        db: Session,
        obj_in: RoleCreateSerializer,
    ) -> Role:
        """Get a role if it exists, otherwise create"""
        role_obj = self.get(db, name=obj_in.name)

        if not role_obj:
            role_obj = self.create(db, obj_in=obj_in)

        return role_obj


role_dao = RoleDao(Role)
