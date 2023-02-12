from pydantic import validator, EmailStr
from typing import Any, Optional
from phonenumbers import parse as parse_phone_number
from phonenumbers import (
    NumberParseException,
    PhoneNumberType,
    is_valid_number,
    number_type
)
from http import HTTPStatus
from app.exceptions.custom import HttpErrorException
from app.errors.custom import ErrorCodes
from email_validator import validate_email
from pyisemail import is_email


PHONE_NUMBER_TYPES = PhoneNumberType.MOBILE, PhoneNumberType.FIXED_LINE_OR_MOBILE


def capitalize_fields(value) -> str:
    """Capitalize first letter of word or string."""
    if isinstance(value, str):
        return value.capitalize()

    return value


def validate_phone_number(phone: str) -> str:
    """Validate str can be parsed into phone number"""
    invalid_phone_number_exception = HttpErrorException(
        status_code=HTTPStatus.BAD_REQUEST,
        error_code=ErrorCodes.INVALID_PHONENUMBER.name,
        error_message=ErrorCodes.INVALID_PHONENUMBER.value.format(
            phone
        ),
    )
    try:
        parsed_phone = parse_phone_number(phone)
    except NumberParseException:
        raise invalid_phone_number_exception

    if (
        number_type(parsed_phone) not in PHONE_NUMBER_TYPES
        or not is_valid_number(parsed_phone)
    ):
        raise invalid_phone_number_exception

    return phone


def validate_email(email: str | None) -> Optional[str]:
    """Validate str is a valid email"""
    if email:
        if not is_email(email):
            raise HttpErrorException(
                status_code=HTTPStatus.BAD_REQUEST,
                error_code=ErrorCodes.INVALID_EMAIL.name,
                error_message=ErrorCodes.INVALID_EMAIL.value.format(
                    email
                ),
            )

    return email
