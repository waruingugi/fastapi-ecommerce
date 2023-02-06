from typing import Optional, Union, Any, Dict

from sqlalchemy.orm import Session

from app.db.dao import CRUDDao
from app.users.models import User
from app.users.serializers.user import UserCreateSerializer, UserUpdateSerializer
from app.users.constants import UserTypes
from app.core.security import get_password_hash, verify_password


class UserDao(CRUDDao[User, UserCreateSerializer, UserUpdateSerializer]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_phone(self, db: Session, *, phone: str) -> Optional[User]:
        return db.query(User).filter(User.phone == phone).first()

    def create(self, db: Session, *, obj_in: UserCreateSerializer):
        create_user_data = obj_in.dict()
        create_user_data.pop("password")

        db_obj = UserCreateSerializer(**create_user_data)
        db_obj.hashed_password = get_password_hash(obj_in.password)

        db.add(db_obj)
        db.commit()
        return db_obj

    def authenticate_user(
        self, db: Session, *, phone: str, password: str
    ):
        user = self.get_by_phone(db, phone)
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdateSerializer, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_superuser(self, user: User) -> bool:
        return user.user_type is UserTypes.SUPERADMIN.value

user_dao = UserDao(User)
