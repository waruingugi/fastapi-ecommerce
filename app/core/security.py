from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.core.config import settings

# from app.auth.serializers.auth import TokenData
from jose import JWTError, jwt
from sqlalchemy.orm import Session, load_only
from app.auth.daos.token import token_dao
from app.roles.daos.user_role import user_role_dao
from app.roles.models import UserRole
from app.auth.models import AuthToken
from app.auth.serializers.token import TokenGrantType, TokenCreateSerializer
from app.auth.utils.token import check_refresh_token_is_valid
from app.auth.serializers.token import TokenReadSerializer
from app.exceptions.custom import ExpiredRefreshToken, InvalidToken
from pydantic import ValidationError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def get_access_token(db: Session, *, user_id: str) -> AuthToken:
    """Creates access token and saves it to ´AuthToken´ model"""
    token_data = create_access_token(
        db=db, subject=user_id, grant_type=TokenGrantType.CLIENT_CREDENTIALS.value
    )

    obj_in = TokenCreateSerializer(
        user_id=user_id,
        token_type=TokenGrantType.CLIENT_CREDENTIALS,
        access_token=token_data["access_token"],
        refresh_token=token_data["refresh_token"],
        refresh_token_eat=datetime.utcnow()
        + timedelta(seconds=token_data["refresh_ein"]),
        access_token_eat=datetime.utcnow()
        + timedelta(seconds=token_data["access_token_ein"]),
        is_active=True,
    )

    return token_dao.create(db, obj_in=obj_in)


def get_decoded_refresh_token(
    db: Session,
    token: str,
) -> dict:
    """Decode the token"""
    if check_refresh_token_is_valid(db, refresh_token=token):
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
                options={"verify_exp": True},
            )

            return payload
        except (JWTError, ValidationError):
            raise InvalidToken
    else:
        raise ExpiredRefreshToken


def renew_access_token(db: Session, *, token: str):
    """Generate new access token if refresh token is valid."""
    token_payload = get_decoded_refresh_token(db, token)
    token = get_access_token(db, user_id=token_payload["user_id"])
    token_dict = {
        "user_id": token.user_id,
        "access_token": token.access_token,
        "refresh_token": token.refresh_token,
        "exp": token.access_token_eat,
        "token_type": "bearer",
    }

    return TokenReadSerializer(**token_dict)


def create_access_token(db: Session, subject: str, grant_type: str) -> dict:
    "Create access token and refresh token"
    access_token_ein = settings.ACCESS_TOKEN_EXPIRY_IN_SECONDS
    refresh_ein = settings.REFRESH_TOKEN_EXPIRY_IN_SECONDS

    to_encode = {
        "iat": int(datetime.utcnow().timestamp()),
        "exp": datetime.utcnow() + timedelta(seconds=access_token_ein),
        "user_id": str(subject),
        "grant_type": grant_type,
    }

    # Add role to token
    user_role = user_role_dao.get_not_none(
        db,
        user_id=to_encode["user_id"],
        load_options=[load_only(UserRole.role_id)],
    )
    to_encode["role_id"] = user_role.role_id

    # Create access token
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    # Create refresh token
    to_encode["exp"] = datetime.utcnow() + timedelta(seconds=refresh_ein)
    to_encode["iat"] = int(datetime.utcnow().timestamp())

    refresh_token = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    token_data = {
        "access_token": token,
        "refresh_token": refresh_token,
        "token_type": grant_type,
        "access_token_ein": access_token_ein,
        "refresh_ein": refresh_ein,
        "user_id": subject,
    }
    return token_data
