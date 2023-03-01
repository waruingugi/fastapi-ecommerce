from typing import Generator, AsyncGenerator, List

from app.db.session import SessionLocal, AsyncSessionLocal
from app.db.permissions import BasePermission
from fastapi import Depends, Response, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
)
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError
from app.users.daos.user import user_dao
from sqlalchemy.orm import Session
from app.core.config import settings
from app.exceptions.custom import (
    InsufficientUserPrivileges,
    InactiveAccount,
    ExpiredRefreshToken,
    ExpiredAccessToken,
    IncorrectCredentials,
    InvalidToken,
    AccessDenied
)
from app.users.models import User
from app.auth.utils.token import (
    check_refresh_token_is_valid,
    check_access_token_is_valid
)
from app.roles.daos.user_role import user_role_dao

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


async def get_decoded_token(
    response: Response,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> dict:
    """Decode the token"""

    if check_access_token_is_valid(db, access_token=token):
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
                options={"verify_exp": True}
            )
            
            # ´x-user-id´ response header is used in logging
            response.headers["x-user-id"] = payload["user_id"]
            return payload
        except (JWTError, ValidationError):
            raise InvalidToken
    else:
        raise ExpiredAccessToken


async def get_current_user(
    security_scopes: SecurityScopes,
    db: Session = Depends(get_db),
    token_payload: dict = Depends(get_decoded_token),
) -> User:
    user = user_dao.get(db, id=token_payload["user_id"])

    if user is None:
        raise IncorrectCredentials

    for scope in security_scopes.scopes:
        if scope not in token_payload["scopes"]:
            raise InsufficientUserPrivileges

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


class Permissions:
    def __init__(self, *perms: BasePermission) -> None:
        self.perms = perms

    async def __call__(
        self,
        db: Session = Depends(get_db),
        token_payload: dict = Depends(get_decoded_token)
    ):
        role = user_role_dao.get(db, user_id=token_payload["user_id"])

        required_perms = [perm.value for perm in self.perms]

        for perm in required_perms:
            if perm not in role.permissions:
                raise AccessDenied
