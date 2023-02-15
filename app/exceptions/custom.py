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
