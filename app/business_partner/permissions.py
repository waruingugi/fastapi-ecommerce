from app.db.permissions import BasePermission


class BusinessPartnerPermissions(BasePermission):
    business_partner_create = "business_partner:create"
    business_partner_read = "business_partner:read"
    business_partner_update = "business_partner:update"
    business_partner_list = "business_partner:list"
