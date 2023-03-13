from typing import Generator, AsyncGenerator

from app.db.session import SessionLocal, AsyncSessionLocal
from app.db.permissions import BasePermission
from fastapi import Depends, Response, Security
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel, ValidationError
from app.users.daos.user import user_dao
from sqlalchemy.orm import Session, load_only
from app.core.config import settings
from app.exceptions.custom import (
    InsufficientUserPrivileges,
    InactiveAccount,
    ExpiredAccessToken,
    IncorrectCredentials,
    InvalidToken,
    AccessDenied,
)
from app.users.models import User
from app.auth.utils.token import check_access_token_is_valid
from app.roles.daos.role import role_dao

from app.commons.filters import CountryScopeFilter
from fastapi_sqlalchemy_filter import Filter


class TokenData(BaseModel):
    username: str | None = None


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/access-token",
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
                options={"verify_exp": True},
            )

            # ´x-user-id´ response header is used in logging
            response.headers["x-user-id"] = payload["user_id"]
            return payload
        except (JWTError, ValidationError):
            raise InvalidToken
    else:
        raise ExpiredAccessToken


async def get_current_user(
    db: Session = Depends(get_db),
    token_payload: dict = Depends(get_decoded_token),
) -> User:
    user = user_dao.get(
        db,
        id=token_payload["user_id"],
        load_options=[load_only(User.id)],
    )

    if user is None:
        raise IncorrectCredentials

    return user


async def get_current_active_user(
    current_user: User = Security(get_current_user),
) -> User:
    if not current_user.is_active:
        raise InactiveAccount
    return current_user


async def get_current_active_superuser(
    current_user: User = Security(get_current_user),
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
        token_payload: dict = Depends(get_decoded_token),
    ):
        role = role_dao.get_not_none(db, id=token_payload["role_id"])

        required_perms = [perm.value for perm in self.perms]

        for perm in required_perms:
            if perm not in role.permissions:
                raise AccessDenied


class RestrictBusinessPartnerFilter:
    def __init__(
        self,
        db: Session = Depends(get_db),
        token: dict = Depends(get_decoded_token),
    ) -> None:
        self.db = db
        self.token = token

    def __call__(self, *, search_filter) -> Filter:
        """Restrict Business Partner Filter or Query based on scope
        *** Note: This depends on the existence of owner field in filter ***"""
        if hasattr(search_filter, "owner"):
            search_filter.owner.country = CountryScopeFilter(
                iso3_code__in=self.token["scope"]
            )

        return search_filter


class RestrictUserFilter:
    def __init__(
        self,
        db: Session = Depends(get_db),
        token: dict = Depends(get_decoded_token),
    ) -> None:
        self.db = db
        self.token = token

    def __call__(self, *, search_filter) -> Filter:
        """Restrict User Filter or Query based on scope
        *** Note: This depends on the existence of country filter ***
        """
        if hasattr(search_filter, "country"):
            search_filter.country.iso3_code__in = self.token["scope"]

        return search_filter
