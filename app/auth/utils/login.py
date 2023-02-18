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


def get_access_token(db: Session, *, user_id: str) -> AuthToken:
    token_data = create_access_token(
        db=db,
        subject=user_id,
        grant_type=TokenGrantType.CLIENT_CREDENTIALS.value
    )

    obj_in = TokenCreateSerializer(
        **token_data,
        token_type=TokenGrantType.CLIENT_CREDENTIALS,
        expires_at=datetime.utcnow() + timedelta(seconds=token_data["expires_ind"]),
        is_active=True
    )

    return  token_dao.create(db, obj_in=obj_in)


def login_user(db: Session, login_data: LoginSerializer) -> TokenReadSerializer:
    user = user_dao.authenticate_user(
        db, username=login_data.username, password=login_data.password
    )

    if not user:
        raise 

