from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.core.config import settings
from jose import jwt
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
)
from fastapi import Depends, FastAPI, HTTPException, Security, status
# from app.auth.serializers.auth import TokenData
from jose import JWTError, jwt
from sqlalchemy.orm import Session



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def create_access_token(
    db: Session, subject: str, grant_type: str
) -> dict:
    "Create access token and refresh token"
    expires_in_seconds =  settings.ACCESS_TOKEN_EXPIRY_IN_SECONDS
    refresh_expires_in_seconds = settings.REFRESH_TOKEN_EXPIRY_IN_SECONDS

    to_encode = {
        "iat": int(datetime.utcnow().timestamp()),
        "exp": datetime.utcnow() + timedelta(seconds=expires_in_seconds),
        "user_id": str(subject),
        "grant_type": grant_type
    }

    # Create access token
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    # Create refresh token
    to_encode["exp"] = datetime.utcnow() + timedelta(seconds=refresh_expires_in_seconds)
    to_encode["iat"] = int(datetime.utcnow().timestamp())

    refresh_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    token_data = {
        "access_token": token,
        "refresh_token": refresh_token,
        "token_type": grant_type,
        "expires_in": expires_in_seconds,
        "refresh_expires_in": refresh_expires_in_seconds,
        "user_id": subject,
    }
    return token_data


# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()

#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(
#             seconds=settings.ACCESS_TOKEN_EXPIRY_IN_SECONDS
#         )
    
#     refresh_expires_in_seconds = settings.REFRESH_TOKEN_EXPIRY_IN_SECONDS

#     to_encode.update({
#         "iat": int(datetime.utcnow().timestamp()),
#         "exp": expire
#     })
#     token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

#     # Create refresh token also
#     to_encode["exp"] = datetime.utcnow() + timedelta(
#         seconds=refresh_expires_in_seconds
#     )
#     to_encode["iat"] = int(datetime.utcnow().timestamp())

#     refresh_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
#     token_data = {
#         "access_token": token,
#         "refresh_token": refresh_token,
#         "token_type": data["grant_type"],
#         "expires_in": settings.ACCESS_TOKEN_EXPIRY_IN_SECONDS,
#         "refresh_token_ein": refresh_expires_in_seconds,
#         "sub": data["sub"],
#     }

#     return token_data
