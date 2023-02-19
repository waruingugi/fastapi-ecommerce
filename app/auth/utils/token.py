from sqlalchemy.orm import Session
from app.auth.daos.token import token_dao
from datetime import datetime


def check_refresh_token_is_valid(db: Session, refresh_token: str) -> bool:
    token_obj = token_dao.get(db, refresh_token=refresh_token)

    return (
        True if token_obj and token_obj.refresh_token_is_valid else False
    )


def check_access_token_is_valid(db: Session, access_token: str) -> bool:
    token_obj = token_dao.get(db, access_token=access_token)

    token_eat = token_obj.access_token_eat if token_obj else None
    return token_eat is not None and token_eat >= datetime.utcnow()
