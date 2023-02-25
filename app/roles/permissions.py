from app.db.permissions import BasePermission
from typing import List
from app.business_partner.permissions import BusinessPartnerPermissions
from app.users.permissions import UserPermissions
from enum import Enum


AdminPermissions: List[BasePermission] = (
    BusinessPartnerPermissions.list_()
    + UserPermissions.list_()
)

CorePermissions: List[str] = [
    UserPermissions.user_read.value,
    UserPermissions.user_update.value,
    BusinessPartnerPermissions.business_partner_create.value,
    BusinessPartnerPermissions.business_partner_read.value
]