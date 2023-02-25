from fastapi import HTTPException
from http import HTTPStatus
from app.errors.custom import ErrorCodes


class HttpErrorException(HTTPException):
    def __init__(self, status_code: int, error_code: str, error_message: str) -> None:
        self.status_code = status_code
        self.error_code = error_code
        self.error_message = error_message
        self.detail = error_message


class IncorrectCredentials(HttpErrorException):
    def __init__(self) -> None:
        super(IncorrectCredentials, self).__init__(
            status_code=HTTPStatus.UNAUTHORIZED,
            error_code=ErrorCodes.INCORRECT_USERNAME_OR_PASSWORD.name,
            error_message=ErrorCodes.INCORRECT_USERNAME_OR_PASSWORD.value,
        )


class InsufficientUserPrivileges(HttpErrorException):
    def __init__(self) -> None:
        super(InsufficientUserPrivileges, self).__init__(
            status_code=HTTPStatus.BAD_REQUEST,
            error_code=ErrorCodes.USERS_PRIVILEGES_NOT_ENOUGH.name,
            error_message=ErrorCodes.USERS_PRIVILEGES_NOT_ENOUGH.value
        )


class InactiveAccount(HttpErrorException):
    def __init__(self) -> None:
        super(InactiveAccount, self).__init__(
            status_code=HTTPStatus.UNAUTHORIZED,
            error_code=ErrorCodes.INACTIVE_ACCOUNT.name,
            error_message=ErrorCodes.INACTIVE_ACCOUNT.value
        )


class ExpiredRefreshToken(HttpErrorException):
    def __init__(self) -> None:
        super(ExpiredRefreshToken, self).__init__(
            status_code=HTTPStatus.UNAUTHORIZED,
            error_code=ErrorCodes.EXPIRED_REFRESH_TOKEN.name,
            error_message=ErrorCodes.EXPIRED_REFRESH_TOKEN.value,
        )


class ExpiredAccessToken(HttpErrorException):
    def __init__(self) -> None:
        super(ExpiredAccessToken, self).__init__(
            status_code=HTTPStatus.UNAUTHORIZED,
            error_code=ErrorCodes.EXPIRED_AUTHORIZATION_TOKEN.name,
            error_message=ErrorCodes.EXPIRED_AUTHORIZATION_TOKEN.value,
        )


class InvalidToken(HttpErrorException):
    def __init__(self) -> None:
        super(InvalidToken, self).__init__(
            status_code=HTTPStatus.UNAUTHORIZED,
            error_code=ErrorCodes.INVALID_TOKEN.name,
            error_message=ErrorCodes.INVALID_TOKEN.value,
        )


class UserDoesNotExist(HttpErrorException):
    def __init__(self) -> None:
        super(UserDoesNotExist, self).__init__(
            status_code=HTTPStatus.NOT_FOUND,
            error_code=ErrorCodes.USER_NOT_FOUND.name,
            error_message=ErrorCodes.USER_NOT_FOUND.value,
        )


class ObjectDoesNotExist(Exception):
    """The specified object was not found"""
    def __init__(self, message: str) -> None:
        self.message = message


class InvalidUserScopeType(Exception):
    """The specified scope was not found in ´UserScopeTypes´"""
    def __init__(self, message: str) -> None:
        self.message = message
