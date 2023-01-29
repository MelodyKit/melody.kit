from typing import Optional
from uuid import UUID

from async_extensions.blocking import run_blocking_in_thread
from email_validator import EmailNotValidError, validate_email  # type: ignore
from fastapi import Body
from fastapi.requests import Request
from jwt import DecodeError, ExpiredSignatureError

from melody.kit.constants import SPACE
from melody.kit.errors import AuthenticationError, ErrorCode, ValidationError
from melody.kit.tokens import decode_token

__all__ = (
    "token_dependency",
    "optional_token_dependency",
    "email_dependency",
    "email_deliverability_dependency",
)

AUTHORIZATION = "Authorization"

AUTHENTICATION_INVALID = "authentication is invalid"
AUTHENTICATION_MISSING = "authentication is missing"
AUTHENTICATION_EXPIRED = "authentication has expired"


def token_dependency(request: Request) -> UUID:
    header = request.headers.get(AUTHORIZATION)

    if header is None:
        raise AuthenticationError(AUTHENTICATION_MISSING, ErrorCode.AUTHENTICATION_MISSING)

    _, _, token = header.partition(SPACE)

    if not token:
        raise AuthenticationError(AUTHENTICATION_INVALID, ErrorCode.AUTHENTICATION_INVALID)

    try:
        user_id = decode_token(token)

    except (DecodeError, KeyError, ValueError):
        raise AuthenticationError(
            AUTHENTICATION_INVALID, ErrorCode.AUTHENTICATION_INVALID
        ) from None

    except ExpiredSignatureError:
        raise AuthenticationError(
            AUTHENTICATION_EXPIRED, ErrorCode.AUTHENTICATION_EXPIRED
        ) from None

    return user_id


def optional_token_dependency(request: Request) -> Optional[UUID]:
    try:
        return token_dependency(request)

    except AuthenticationError:
        return None


INVALID_EMAIL = "email `{}` is invalid"


def email_dependency(email: str = Body()) -> str:
    try:
        result = validate_email(email, check_deliverability=False)

    except EmailNotValidError:
        raise ValidationError(INVALID_EMAIL.format(email))

    return result.email  # type: ignore


async def email_deliverability_dependency(email: str = Body()) -> str:
    try:
        result = await run_blocking_in_thread(validate_email, email, check_deliverability=True)

    except EmailNotValidError:
        raise ValidationError(INVALID_EMAIL.format(email))

    return result.email  # type: ignore
