from app.db.permissions import BasePermission
from typing import List
from app.business_partner.permissions import BusinessPartnerPermissions
from app.users.permissions import UserPermissions
from app.roles.permissions import UserRolePermissions, RolePermissions
from app.common.permissions import CurrencyPermissions

# Organize Permissions in hierarchy structure
# The UserType Roles are written here to serve as a template
# when adding values using the API
CorePermissions: List[str] = [
    BusinessPartnerPermissions.business_partner_read.value,
    CurrencyPermissions.currency_read.value,
    CurrencyPermissions.currency_list.value,
]

CustomerPermissions: List[str] = [
    BusinessPartnerPermissions.business_partner_read.value,
    CurrencyPermissions.currency_read.value,
    CurrencyPermissions.currency_list.value,
]

AdminPermissions: List[str] = [
    UserRolePermissions.user_role_list.value,
    UserRolePermissions.user_role_read.value,
    RolePermissions.role_list.value,
    RolePermissions.role_read.value,
]
AdminPermissions += (
    BusinessPartnerPermissions.list_()
    + UserPermissions.list_()
    + CurrencyPermissions.list_()
)

AllAppPermissions: List[BasePermission] = (
    BusinessPartnerPermissions.list_()
    + UserPermissions.list_()
    + UserRolePermissions.list_()
    + RolePermissions.list_()
    + CurrencyPermissions.list_()
)

SuperAdminPermissions: List[BasePermission] = AllAppPermissions
