from enum import Enum
from typing import List


class BasePermission(str, Enum):
    def entity(self) -> str:
        return self.value.split(":")[0]

    def action(self) -> str:
        return self.value.split(":")[1]

    @classmethod
    def list_(cls) -> List:
        perms = {permission.value for permission in cls}
        return list(perms)
    
    @classmethod
    def description(cls) -> str:
        return ""
