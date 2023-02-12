from typing import Optional
from uuid import UUID

from async_extensions.blocking import run_blocking_in_thread
from email_validator import EmailNotValidError, validate_email  # type: ignore
from fastapi import Form
from fastapi.requests import Request

from melody.kit.errors import AuthenticationError, ErrorCode, ValidationError
from melody.kit.tokens import fetch_token
from melody.web.constants import TOKEN

__all__ = ("cookie_token_dependency", "optional_cookie_token_dependency")

AUTHENTICATION_MISSING = "authentication is missing"
AUTHENTICATION_INVALID = "authentication is invalid"
AUTHENTICATION_EXPIRED = "authentication has expired"


async def cookie_token_dependency(request: Request) -> UUID:
    cookies = request.cookies

    token = cookies.get(TOKEN)

    if token is None:
        raise AuthenticationError(AUTHENTICATION_MISSING, ErrorCode.AUTHENTICATION_MISSING)

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


async def optional_cookie_token_dependency(request: Request) -> Optional[UUID]:
    try:
        return await cookie_token_dependency(request)

    except AuthenticationError:
        return None


INVALID_EMAIL = "email `{}` is invalid"


def form_email_dependency(email: str = Form()) -> str:
    try:
        result = validate_email(email, check_deliverability=False)

    except EmailNotValidError:
        raise ValidationError(INVALID_EMAIL.format(email))

    return result.email  # type: ignore


async def form_email_deliverability_dependency(email: str = Form()) -> str:
    try:
        result = await run_blocking_in_thread(validate_email, email, check_deliverability=True)

    except EmailNotValidError:
        raise ValidationError(INVALID_EMAIL.format(email))

    return result.email  # type: ignore
