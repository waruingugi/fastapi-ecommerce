from typing import Optional, Union, Any, Dict

from sqlalchemy.orm import Session

from app.db.dao import CRUDDao
from app.users.models import User
from app.roles.daos.role import role_dao
from app.roles.daos.user_role import user_role_dao
from app.roles.serializers.user_role import (
    UserRoleCreateSerializer,
)
from app.users.serializers.user import (
    UserCreateSerializer,
    UserUpdateSerializer,
    UserBaseSerializer,
)
from app.users.constants import UserTypes
from app.core.security import get_password_hash, verify_password
from pyisemail import is_email
from typing import List


class UserDao(CRUDDao[User, UserCreateSerializer, UserUpdateSerializer]):
    def on_post_create(self, db: Session, db_obj: Union[User, List[User]]) -> None:
        if isinstance(db_obj, User):
            db_obj = [db_obj]
        for user in db_obj:
            """Create a role that enables the user to access endpoints"""
            role = role_dao.get_not_none(db, name=user.user_type)

            user_role_dao.create(
                db,
                obj_in=UserRoleCreateSerializer(
                    user_id=user.id, role_id=role.id, scope=[user.country.iso3_code]
                ),
            )

    def on_post_update(self, db: Session, db_obj: User, changed: Dict) -> None:
        if changed.get("user_type", None):
            """Update the role that enables the user to access endpoints"""
            role = role_dao.get_not_none(db, name=changed["user_type"]["after"])
            user_role = user_role_dao.get(db, user_id=db_obj.id)

            user_role_dao.update(db, db_obj=user_role, obj_in={"role_id": role.id})

    def get_by_phone_or_email(
        self, db: Session, *, email: Optional[str] = None, phone: Optional[str] = None
    ) -> Optional[User]:
        if email:
            return self.get_by_username(db, username=email)

        if phone:
            return self.get_by_username(db, username=phone)
        return None

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        if is_email(username):
            return self.get(db, email=username)
        else:
            return self.get(db, phone=username)

    def get_or_create(
        self,
        db: Session,
        obj_in: Union[UserBaseSerializer, UserCreateSerializer],
    ) -> User:
        """Get or create a user"""
        user_in = user_dao.get_by_phone_or_email(
            db, email=obj_in.email, phone=obj_in.phone
        )
        if not user_in:
            user_data = UserCreateSerializer(**obj_in.dict())
            user_in = self.create(db, obj_in=user_data)

        return user_in

    def create(self, db: Session, *, obj_in: UserCreateSerializer) -> User:
        create_user_data = obj_in.dict()
        create_user_data.pop("password")

        db_obj = User(**create_user_data)
        db_obj.hashed_password = get_password_hash(obj_in.password)

        db.add(db_obj)
        db.commit()

        db_obj = self.get_not_none(db, phone=db_obj.phone)
        self.on_post_create(db, db_obj)

        return db_obj

    def authenticate_user(self, db: Session, *, username: str, password: str):
        user = self.get_by_username(db, username=username)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

    def update(
        self,
        db: Session,
        *,
        db_obj: User,
        obj_in: Union[UserUpdateSerializer, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if update_data.get("password", None):
            update_data["hashed_password"] = get_password_hash(update_data["password"])

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_superuser(self, user: User) -> bool:
        return user.user_type == UserTypes.SUPERADMIN.value


user_dao = UserDao(User)
