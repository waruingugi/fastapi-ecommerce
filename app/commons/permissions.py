from app.db.permissions import BasePermission


class CurrencyPermissions(BasePermission):
    currency_create = "currency:create"
    currency_read = "currency:read"
    currency_update = "currency:update"
    currency_list = "currency:list"


class CountryPermissions(BasePermission):
    country_create = "country:create"
    country_read = "country:read"
    country_update = "country:update"
    country_list = "country:list"
