from typing import Optional
from uuid import UUID

from async_extensions.blocking import run_blocking_in_thread
from email_validator import EmailNotValidError, validate_email  # type: ignore
from fastapi import Body
from fastapi.requests import Request

from melody.kit.errors import AuthenticationError, ErrorCode, ValidationError
from melody.kit.tokens import fetch_token
from melody.shared.constants import SPACE

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


async def token_dependency(request: Request) -> UUID:
    header = request.headers.get(AUTHORIZATION)

    if header is None:
        raise AuthenticationError(AUTHENTICATION_MISSING, ErrorCode.AUTHENTICATION_MISSING)

    _, _, token = header.partition(SPACE)

    if not token:
        raise AuthenticationError(AUTHENTICATION_INVALID, ErrorCode.AUTHENTICATION_INVALID)

    try:
        user_id = await fetch_token(token)

    except LookupError:
        raise AuthenticationError(
            AUTHENTICATION_INVALID, ErrorCode.AUTHENTICATION_INVALID
        ) from None

    except TimeoutError:
        raise AuthenticationError(
            AUTHENTICATION_EXPIRED, ErrorCode.AUTHENTICATION_EXPIRED
        ) from None

    return user_id


async def optional_token_dependency(request: Request) -> Optional[UUID]:
    try:
        return await token_dependency(request)

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
