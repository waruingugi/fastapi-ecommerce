from enum import Enum
from typing import List


class UserTypes(str, Enum):  # Also acts as role names
    SUPERADMIN = "SUPERADMIN"
    ADMIN = "ADMIN"
    BUSINESS_OWNER = "BUSINESS_OWNER"
    BUSINESS_EMPLOYEE = "BUSINESS_EMPLOYEE"
    CUSTOMER = "CUSTOMER"
    CALL_CENTRE_AGENT = "CALL_CENTRE_AGENT"

    @classmethod
    def list_(cls) -> List:
        user_type = {type.value for type in cls}
        return list(user_type)
