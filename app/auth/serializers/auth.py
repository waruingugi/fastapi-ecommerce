from pydantic import BaseModel
from typing import List


class TokenData(BaseModel):
    phone: str | None = None
    scopes: List[str] = []
