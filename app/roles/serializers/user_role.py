from app.db.serializer import InDBBaseSerializer
from pydantic import BaseModel
from app.users.serializers.user import UserReadSerializer


class UserRoleBaseSerializer(BaseModel):
    user_id: str
    role_id: str


class UserRoleInDBSerializer(InDBBaseSerializer, UserRoleBaseSerializer):
    user: UserReadSerializer


class UserRoleCreateSerializer(UserRoleBaseSerializer):
    ...


class UserRoleUpdateSerializer(UserRoleBaseSerializer):
    user_id: str | None
    role_id: str | None
