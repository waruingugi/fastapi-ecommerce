from enum import Enum
from typing import List


class BasePermission(str, Enum):
    def entity(self) -> str:
        return self.value.split(":")[0]

    def action(self) -> str:
        return self.value.split(":")[1]

    @classmethod
    def list(cls) -> List:
        return [permission for permission in cls]


class UserScopeTypes(str, Enum):
    MARKETPLACE = "MARKETPLACE"
    COUNTRY = "COUNTRY"
    REGION = "REGION"
    AREA = "AREA"
