from enum import Enum


class UserScopeTypes(str, Enum):
    MARKETPLACE = "MARKETPLACE"
    COUNTRY = "COUNTRY"
    REGION = "REGION"
    AREA = "AREA"
