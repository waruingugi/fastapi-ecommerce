from app.auth.serializers.token import (
    TokenCreateSerializer,
    TokenInDBSerializer
)
from app.db.dao import CRUDDao
from app.auth.models import AuthToken
from sqlalchemy.orm import Session


class TokenDao(
    CRUDDao[AuthToken, TokenCreateSerializer, TokenInDBSerializer]
):
    def on_pre_create(
        self, db: Session, id: str, values: dict, orig_values: dict
    ) -> None:
        values["token_type"] = orig_values["token_type"].value


token_dao = TokenDao(AuthToken)
