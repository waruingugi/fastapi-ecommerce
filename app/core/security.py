from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.core.config import get_app_settings
from jose import jwt
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
)
from fastapi import Depends, FastAPI, HTTPException, Security, status
from app.core.config import get_app_settings
# from app.auth.serializers.auth import TokenData
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.users.serializers.user import UserBaseSerializer


settings = get_app_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            seconds=settings.ACCESS_TOKEN_EXPIRY_IN_SECONDS
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt
