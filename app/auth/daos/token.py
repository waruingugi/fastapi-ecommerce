from app.auth.serializers.token import (
    TokenCreateSerializer,
    TokenInDbSerializer
)
from app.db.dao import CRUDDao
from app.auth.models import AuthToken


class TokenDao(
    CRUDDao[AuthToken, TokenCreateSerializer, TokenInDbSerializer]
):
    pass


token_dao = TokenDao(AuthToken)
