from enum import Enum
from app.auth.permissions import (
    AdminPermissions,
    CustomerPermissions,
    SuperAdminPermissions
)


class UserScopeTypes(str, Enum):
    MARKETPLACE = "MARKETPLACE"
    COUNTRY = "COUNTRY"
    REGION = "REGION"
    AREA = "AREA"


class UserRolePermissions(Enum):
    SUPERADMIN = SuperAdminPermissions
    ADMIN = AdminPermissions
    CUSTOMER = CustomerPermissions
