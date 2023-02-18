from sqlalchemy.orm import Session
from app.auth.daos.token import token_dao


def check_refresh_token_is_valid(db: Session, token: str) -> bool:
    token_obj = token_dao.get(db, refresh_token=token)

    