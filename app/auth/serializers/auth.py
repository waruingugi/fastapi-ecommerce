from pydantic import BaseModel


class LoginSerializer(BaseModel):
    username: str
    password: str
