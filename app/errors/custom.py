from enum import Enum


class ErrorCodes(str, Enum):
    INVALID_PHONENUMBER = "The phone number {} is not valid"
    INVALID_EMAIL = "The email {} is not valid. Please try another"
    NO_CHANGES_DETECTED = "No changes were detected"
    USERNAME_ALREADY_EXISTS = "A user with this username already exists in the system"
    BUSINESS_OWNER_DOES_NOT_EXIST = "The owner for this business does not exist. Did you create the owner?"
    INCORRECT_USERNAME_OR_PASSWORD = "Incorrect username or password"
