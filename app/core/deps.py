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
from app.core.config import get_app_settings


class TokenData(BaseModel):
    phone: str | None = None
    scopes: List[str] = []



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
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
):
    settings = get_app_settings()
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
        phone: str = payload.get("sub")
        if phone is None:
            raise credentials_exception

        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, phone=phone)

    except (JWTError, ValidationError):
        raise credentials_exception

    user = user_dao.get_by_phone(db, phone=token_data.phone)

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
    current_user: UserBaseSerializer = Security(get_current_user, scopes=["me"])
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
