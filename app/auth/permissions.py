from app.db.permissions import BasePermission
from typing import List
from app.business_partner.permissions import BusinessPartnerPermissions
from app.users.permissions import UserPermissions
from enum import Enum
from app.roles.permissions import UserRolePermissions

# Organize Permissions in hierarchy structure
CorePermissions: List[str] = [
    BusinessPartnerPermissions.business_partner_read.value
]


CustomerPermissions: List[str] = [
    BusinessPartnerPermissions.business_partner_read.value,
]


AdminPermissions: List[BasePermission] = (
    BusinessPartnerPermissions.list_()
    + UserPermissions.list_()
    + UserRolePermissions.list_()
)


SuperAdminPermissions: List[BasePermission] = (
    AdminPermissions
)
