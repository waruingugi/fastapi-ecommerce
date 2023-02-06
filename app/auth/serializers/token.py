from pydantic import BaseModel


class TokenBaseSerializer(BaseModel):
    access_token: str
    token_type: str
