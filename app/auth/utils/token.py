from sqlalchemy.orm import Session
from app.auth.daos.token import token_dao


def check_refresh_token_is_valid(db: Session, refresh_token: str) -> bool:
    token_obj = token_dao.get(db, refresh_token=refresh_token)

    return (
        True if token_obj and token_obj.refresh_token_is_valid else False
    )


def check_access_token_is_valid(db: Session, access_token: str) -> bool:
    token_obj = token_dao.get(db, access_token=token)

    return (
        True if token_obj and token_obj.access_token_is_valid else False
    )
