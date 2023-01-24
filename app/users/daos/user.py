from typing import Optional, Union, Any, Dict

from sqlalchemy.orm import Session

from app.db.dao import CRUDBase
from app.users.models import User
from app.users.serailizers.user import UserCreateSerializer, UserUpdateSerializer
from app.users.constants import UserTypes

class UserDao(CRUDBase[User, UserCreateSerializer, UserUpdateSerializer]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    
    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdateSerializer, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_superuser(self, user: User) -> bool:
        return user.user_type is UserTypes.ADMIN.value

user_dao = UserDao(User)
