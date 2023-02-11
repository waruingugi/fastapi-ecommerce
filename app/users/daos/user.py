from typing import Optional, Union, Any, Dict

from sqlalchemy.orm import Session

from app.db.dao import CRUDDao
from app.users.models import User
from app.users.serializers.user import UserCreateSerializer, UserUpdateSerializer
from app.users.constants import UserTypes
from app.core.security import get_password_hash, verify_password
from app.core.helpers import validate_email


class UserDao(CRUDDao[User, UserCreateSerializer, UserUpdateSerializer]):
    # def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
    #     return db.query(User).filter(User.email == email).first()

    # def get_by_phone(self, db: Session, phone: str) -> Optional[User]:
    #     return db.query(User).filter(User.phone == phone).first()
    def on_pre_create(
        self, db: Session, pk: str, values: dict, orig_values: dict
    ) -> None:
        if "password" in orig_values:
            values["hashed_password"] = get_password_hash(orig_values["password"])

    def get_by_phone_or_email(
        self, db: Session, *, email: Optional[str] = None, phone: Optional[str] = None
    ) -> Optional[User]:
        if email:
            return self.get_by_username(db, username=email)

        if phone:
            return self.get_by_username(db, username=phone)
        return None

    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        if validate_email(username):
            return self.get(db, email=username)
        else:
            return self.get(db, phone=username)

    def create(self, db: Session, *, obj_in: UserCreateSerializer) -> User:
        create_user_data = obj_in.dict()
        create_user_data.pop("password")

        db_obj = User(**create_user_data)
        db_obj.hashed_password = get_password_hash(obj_in.password)

        db.add(db_obj)
        db.commit()
        return db_obj

    def authenticate_user(
        self, db: Session, *, phone: str, password: str
    ):
        user = self.get_by_username(db, phone=phone)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
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
