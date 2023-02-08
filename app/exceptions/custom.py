from fastapi import HTTPException


class HttpErrorException(HTTPException):
    def __init__(self, status_code: int, error_code: str, error_message: str) -> None:
        self.status_code = status_code
        self.error_code = error_code
        self.error_message = error_message
        self.detail = error_message


class BadFilterFormat(Exception):
    """An invalid operator was used in a query filter."""
    pass


class FieldNotFound(Exception):
    """An invalid column field was used in a query filter."""
    pass
