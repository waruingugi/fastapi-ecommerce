from sqlalchemy.orm import Session, load_only
from app.auth.daos.token import token_dao
from app.auth.models import AuthToken
from datetime import datetime


def check_refresh_token_is_valid(db: Session, refresh_token: str) -> bool:
    token_obj = token_dao.get(
        db,
        refresh_token=refresh_token,
        load_options=[load_only(AuthToken.refresh_token_is_valid)],
    )

    return True if token_obj and token_obj.refresh_token_is_valid else False


def check_access_token_is_valid(db: Session, access_token: str) -> bool:
    token_obj = token_dao.get(
        db,
        access_token=access_token,
        load_options=[load_only(AuthToken.access_token_eat, AuthToken.is_active)],
    )

    token_eat = token_obj.access_token_eat if token_obj else None
    return (
        token_eat is not None
        and token_eat >= datetime.utcnow()
        and bool(token_obj.is_active)
    )
