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
from fastapi import HTTPException
from app.errors.custom import ErrorCodes
from phonenumbers.phonenumber import PhoneNumber
from email_validator import validate_email
from app.exceptions.custom import EmailIsNotValidException
from pyisemail import is_email


PHONE_NUMBER_TYPES = PhoneNumberType.MOBILE, PhoneNumberType.FIXED_LINE_OR_MOBILE


def capitalize_fields(value) -> str:
    """Capitalize first letter of word or string."""
    if isinstance(value, str):
        return value.capitalize()

    return value


def validate_phone_number(phone: str) -> str:
    """Validate str can be parsed into phone number"""
    phone_number_exception = HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail=ErrorCodes.INVALID_PHONENUMBER.value
    )
    try:
        parsed_phone = parse_phone_number(phone)
    except NumberParseException:
        raise phone_number_exception

    if (
        number_type(parsed_phone) not in PHONE_NUMBER_TYPES
        or not is_valid_number(parsed_phone)
    ):
        raise phone_number_exception

    return phone


def validate_email(email: str | None) -> Optional[str]:
    """Validate str is a valid email"""
    if email:
        if not is_email(email):
            raise EmailIsNotValidException()

    return email
