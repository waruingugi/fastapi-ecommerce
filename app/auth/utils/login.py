from app.users.daos.user import user_dao
from app.auth.daos.token import TokenDao
from sqlalchemy.orm import Session
from app.auth.models import AuthToken
from app.core.security import create_access_token
from app.auth.serializers.token import (
    TokenGrantType,
    TokenCreateSerializer,
    TokenReadSerializer
)
from app.auth.serializers.auth import LoginSerializer
from datetime import datetime, timedelta
from app.auth.daos.token import token_dao
from fastapi import Depends
from app.exceptions.custom import IncorrectCredentials, InactiveAccount
from app.core.config import settings


def get_access_token(db: Session, *, user_id: str) -> AuthToken:
    """Creates access token and saves it to ´AuthToken´ model"""
    token_data = create_access_token(
        db=db,
        subject=user_id,
        grant_type=TokenGrantType.CLIENT_CREDENTIALS.value
    )

    obj_in = TokenCreateSerializer(
        user_id=user_id,
        access_token=token_data["access_token"],
        refresh_token=token_data["refresh_token"],
        expires_in=token_data["expires_in"],
        token_type=TokenGrantType.CLIENT_CREDENTIALS,
        expires_at=datetime.utcnow() + timedelta(seconds=token_data["expires_in"]),
        is_active=True
    )

    return token_dao.create(db, obj_in=obj_in)


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
        "refresh_token_ein": settings.REFRESH_TOKEN_EXPIRY_IN_SECONDS,
        "token_type": "bearer",
    }

    return TokenReadSerializer(**token_dict)
