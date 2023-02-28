from app.db.permissions import BasePermission


class UserRolePermissions(BasePermission):
    user_role_create = "user_role:create"
    user_role_read = "user_role:read"
    user_role_update = "user_role:update"
    user_role_list = "user_role:list"
