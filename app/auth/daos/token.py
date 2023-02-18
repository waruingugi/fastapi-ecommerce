from app.auth.serializers.token import (
    TokenCreateSerializer,
    TokenInDBSerializer
)
from app.db.dao import CRUDDao
from app.auth.models import AuthToken


class TokenDao(
    CRUDDao[AuthToken, TokenCreateSerializer, TokenInDBSerializer]
):
    pass


token_dao = TokenDao(AuthToken)
