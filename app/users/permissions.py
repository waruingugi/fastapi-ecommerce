from app.auth.constants import BasePermission


class UserPermissions(BasePermission):
    user_create = "user:create"
    user_read = "user:read"
    user_update = "user:update"
    user_list = "user:list"
