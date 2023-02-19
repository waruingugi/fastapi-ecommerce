from app.users.daos.user import user_dao
from app.auth.daos.token import TokenDao
from sqlalchemy.orm import Session
from app.core.security import get_access_token
from app.auth.serializers.token import TokenReadSerializer
from app.auth.serializers.auth import LoginSerializer
from datetime import datetime, timedelta
from fastapi import Depends
from app.exceptions.custom import IncorrectCredentials, InactiveAccount
from app.core.config import settings


def login_user(db: Session, login_data: LoginSerializer) -> TokenReadSerializer:
    """Grants an authenticated user a token"""
    user = user_dao.authenticate_user(
        db, username=login_data.username, password=login_data.password
    )

    if not user:
        raise IncorrectCredentials
    elif not user.is_active:
        raise InactiveAccount

    token = get_access_token(db, user_id=user.id)
    token_dict = {
        "user_id": user.id,
        "access_token": token.access_token,
        "refresh_token": token.refresh_token,
        "exp": token.access_token_eat,
        "token_type": "bearer",
    }

    return TokenReadSerializer(**token_dict)
