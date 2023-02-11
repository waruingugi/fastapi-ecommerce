from enum import Enum


class ErrorCodes(str, Enum):
    INVALID_PHONENUMBER = "Phone number is not valid"
    NO_CHANGES_DETECTED = "No changes were detected"
    USERNAME_ALREADY_EXISTS = "A user with this username already exists in the system"
