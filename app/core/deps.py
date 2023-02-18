from typing import Generator, AsyncGenerator, List

from app.db.session import SessionLocal, AsyncSessionLocal
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
)
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError
from app.users.daos.user import user_dao
from app.users.serializers.user import UserBaseSerializer
from sqlalchemy.orm import Session
from app.core.config import settings
from app.exceptions.custom import InsufficientUserPrivileges, InactiveAccount
from app.users.models import User


class TokenData(BaseModel):
    username: str | None = None
    scopes: List[str] = []



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/access-token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)


def get_db() -> Generator:
    with SessionLocal() as db:
        yield db


async def get_async_db() -> AsyncGenerator:
    async with AsyncSessionLocal() as db:
        yield db


async def get_current_user(
    security_scopes: SecurityScopes,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)

    except (JWTError, ValidationError):
        raise credentials_exception

    user = user_dao.get_by_username(db, username=token_data.username)

    if user is None:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )

    return user


async def get_current_active_user(
    current_user: User = Security(get_current_user)
) -> User:
    if not current_user.is_active:
        raise InactiveAccount
    return current_user


async def get_current_active_superuser(
    current_user: User = Security(get_current_user)
) -> User:
    if not user_dao.is_superuser(current_user):
        raise InsufficientUserPrivileges
    return current_user
