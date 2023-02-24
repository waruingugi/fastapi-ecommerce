from enum import Enum
from app.roles.permissions import AdminPermissions, CorePermissions


class UserScopeTypes(str, Enum):
    MARKETPLACE = "MARKETPLACE"
    COUNTRY = "COUNTRY"
    REGION = "REGION"
    AREA = "AREA"


class UserPermissions(Enum):
    ADMIN = AdminPermissions
    CUSTOMER = CorePermissions
