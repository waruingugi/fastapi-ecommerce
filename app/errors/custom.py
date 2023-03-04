from enum import Enum


class ErrorCodes(str, Enum):
    INVALID_PHONENUMBER = "The phone number {} is not valid"
    INVALID_EMAIL = "The email {} is not valid. Please try another"
    INVALID_BP_VERIFICATION_STATE = "The verification state specified is not recognized"
    NO_CHANGES_DETECTED = "No changes were detected"
    USERNAME_ALREADY_EXISTS = "A user with this username already exists in the system"
    BUSINESS_OWNER_DOES_NOT_EXIST = (
        "The owner of this business does not exist. Did you create the owner?"
    )
    INCORRECT_USERNAME_OR_PASSWORD = "Incorrect username or password"
    USERS_PRIVILEGES_NOT_ENOUGH = "This user doesn't have enough privileges"
    INACTIVE_ACCOUNT = "This account is currently inactive"
    EXPIRED_REFRESH_TOKEN = "The refresh token expired"
    EXPIRED_AUTHORIZATION_TOKEN = "The authorization token expired"
    INVALID_TOKEN = "Could not validate your token"
    USER_NOT_FOUND = "This user does not exist in the system"
    OBJECT_NOT_FOUND = "The specified object does not exist"
    ACCESS_DENIED = "You are not permitted to perform this action"
