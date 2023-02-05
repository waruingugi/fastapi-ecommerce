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
from app.users.daos.user import user_dao
from app.core.deps import get_db
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


def authenticate_user(
    db: Session, *, phone: str, password: str
):
    user = user_dao.get_by_phone(db, phone)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

# async def get_current_user(
#     db: Session = Depends(get_db),
#     security_scopes: SecurityScopes,
#     token: str = Depends(oauth2_scheme)
# ):
#     if security_scopes.scopes:
#         authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
#     else:
#         authenticate_value = "Bearer"

#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": authenticate_value},
#     )

#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         phone: str = payload.get("sub")
#         if phone is None:
#             raise credentials_exception

#         token_scopes = payload.get("scopes", [])
#         token_data = TokenData(scopes=token_scopes, phone=phone)

#     except (JWTError, ValidationError):
#         raise credentials_exception

#     user = user_dao.get_by_phone(db, phone=token_data.phone)

#     if user is None:
#         raise credentials_exception

#     for scope in security_scopes.scopes:
#         if scope not in token_data.scopes:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Not enough permissions",
#                 headers={"WWW-Authenticate": authenticate_value},
#             )

#     return user

# async def get_current_active_user(
#     current_user: UserBaseSerializer = Security(get_current_user, scopes=["me"])
# ):
#     if not current_user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
