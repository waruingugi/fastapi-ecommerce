from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime
from app.db.serializer import InDBBaseSerializer


class TokenGrantType(Enum):
    IMPLICIT = "implict"
    AUTHORIZATION_CODE = "authorization_code"
    CLIENT_CREDENTIALS = "client_credentials"
    PASSWORD = "password"
    REFRESH_TOKEN = "refresh_token"

class TokenBaseSerializer(BaseModel):
    access_token: str
    refresh_token: Optional[str]
    token_type: TokenGrantType
    user_id: str


class TokenReadSerializer(BaseModel):
    user_id: str
    access_token: Optional[str]
    refresh_token: Optional[str]
    token_type: str
    refresh_token_ein: Optional[int]


class TokenCreateSerializer(BaseModel):
    token_type: TokenGrantType
    user_id: str
    access_token: str
    refresh_token: str
    expires_in: int
    expires_at: datetime
    is_active: bool


class TokenInDBSerializer(TokenBaseSerializer, InDBBaseSerializer):
    id: str
    expires_at: datetime
    expires_in: int
    is_active: bool
