from typing import Optional
from uuid import UUID

from async_extensions.blocking import run_blocking_in_thread
from email_validator import EmailNotValidError, validate_email  # type: ignore
from fastapi import Form
from fastapi.requests import Request

from melody.kit.dependencies import BoundToken
from melody.kit.errors import (
    AuthenticationError,
    AuthenticationMissing,
    AuthenticationNotFound,
    ValidationError,
)
from melody.kit.tokens import fetch_user_id_by
from melody.web.constants import TOKEN

__all__ = (
    "bound_cookie_token_dependency",
    "cookie_token_dependency",
    "optional_cookie_token_dependency",
    "form_email_dependency",
    "form_email_deliverability_dependency",
)

AUTHENTICATION_MISSING = "authentication is missing"
AUTHENTICATION_INVALID = "authentication is invalid"
AUTHENTICATION_NOT_FOUND = "authentication not found"


async def bound_cookie_token_dependency(request: Request) -> BoundToken:
    cookies = request.cookies

    token = cookies.get(TOKEN)

    if token is None:
        raise AuthenticationMissing(AUTHENTICATION_MISSING)

    user_id = await fetch_user_id_by(token)

    if user_id is None:
        raise AuthenticationNotFound(AUTHENTICATION_NOT_FOUND)

    return BoundToken(token, user_id)


async def cookie_token_dependency(request: Request) -> UUID:
    bound_token = await bound_cookie_token_dependency(request)

    return bound_token.user_id


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
