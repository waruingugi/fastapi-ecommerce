from pydantic import validator
from typing import Optional, List
from phonenumbers import parse as parse_phone_number
from phonenumbers import (
    NumberParseException,
    PhoneNumberType,
    is_valid_number,
    number_type,
)
from http import HTTPStatus
from app.exceptions.custom import HttpErrorException
from app.errors.custom import ErrorCodes
from pyisemail import is_email

from app.exceptions.custom import InvalidBusinessPartnerVerificationState
from app.business_partner.constants import BusinessPartnerVerificationStates
from hashlib import md5


PHONE_NUMBER_TYPES = PhoneNumberType.MOBILE, PhoneNumberType.FIXED_LINE_OR_MOBILE


def capitalize_fields(value) -> str:
    """Capitalize first letter of word or string."""
    if isinstance(value, str):
        return value.capitalize()

    return value


_capitalize_fields = validator("name", pre=True, allow_reuse=True)(capitalize_fields)


def validate_phone_number(phone: str) -> str:
    """Validate str can be parsed into phone number"""
    invalid_phone_number_exception = HttpErrorException(
        status_code=HTTPStatus.BAD_REQUEST,
        error_code=ErrorCodes.INVALID_PHONENUMBER.name,
        error_message=ErrorCodes.INVALID_PHONENUMBER.value.format(phone),
    )
    try:
        parsed_phone = parse_phone_number(phone)
    except NumberParseException:
        raise invalid_phone_number_exception

    if number_type(parsed_phone) not in PHONE_NUMBER_TYPES or not is_valid_number(
        parsed_phone
    ):
        raise invalid_phone_number_exception

    return phone


_validate_phone_number = validator("phone", pre=True, allow_reuse=True)(
    validate_phone_number
)


def validate_email(email: str | None) -> Optional[str]:
    """Validate str is a valid email"""
    if email:
        if not is_email(email):
            raise HttpErrorException(
                status_code=HTTPStatus.BAD_REQUEST,
                error_code=ErrorCodes.INVALID_EMAIL.name,
                error_message=ErrorCodes.INVALID_EMAIL.value.format(email),
            )

    return email


_validate_email = validator("email", pre=True, allow_reuse=True)(validate_email)


def valid_bp_verification_state(cls, value):
    "Validate business partner verification state"
    bp_verification_states = [
        bp_type.value
        for bp_type in BusinessPartnerVerificationStates.__members__.values()
    ]
    if value not in bp_verification_states:
        raise InvalidBusinessPartnerVerificationState
    return value


_validate_bp_verification_state = validator(
    "verification_state", pre=True, allow_reuse=True
)(valid_bp_verification_state)


def convert_perms_list_to_string(perms_list: List[str]) -> str:
    """Convert permissions list to string"""
    return ", ".join(map(str, set(perms_list))) if perms_list else ""


def md5_hash(value: str) -> str:
    """Convert string value into hash"""
    return md5(value.encode()).hexdigest()
