from app.db.permissions import BasePermission


class UserRolePermissions(BasePermission):
    user_create = "user_role:create"
    user_read = "user_role:read"
    user_update = "user_role:update"
    user_list = "user_role:list"
