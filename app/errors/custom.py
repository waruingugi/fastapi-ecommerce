from enum import Enum


class ErrorCodes(str, Enum):
    INVALID_PHONENUMBER = "Phone number is not valid"
    NO_CHANGES_DETECTED = "No changes were detected"
