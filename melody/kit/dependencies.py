from typing import Optional
from uuid import UUID

from async_extensions.blocking import run_blocking_in_thread
from attrs import define
from email_validator import EmailNotValidError, validate_email  # type: ignore
from fastapi import Body
from fastapi.requests import Request

from melody.kit.errors import (
    AuthenticationError,
    AuthenticationInvalid,
    AuthenticationMissing,
    AuthenticationNotFound,
    ValidationError,
)
from melody.kit.tokens import fetch_user_id_by
from melody.shared.constants import SPACE

__all__ = (
    "BoundToken",
    "bound_token_dependency",
    "token_dependency",
    "optional_token_dependency",
    "email_dependency",
    "email_deliverability_dependency",
)


@define()
class BoundToken:
    token: str
    user_id: UUID


AUTHORIZATION = "Authorization"

AUTHENTICATION_INVALID = "authentication is invalid"
AUTHENTICATION_MISSING = "authentication is missing"
AUTHENTICATION_NOT_FOUND = "authentication not found"


async def bound_token_dependency(request: Request) -> BoundToken:
    header = request.headers.get(AUTHORIZATION)

    if header is None:
        raise AuthenticationMissing(AUTHENTICATION_MISSING)

    _, _, token = header.partition(SPACE)

    if not token:
        raise AuthenticationInvalid(AUTHENTICATION_INVALID)

    user_id = await fetch_user_id_by(token)

    if user_id is None:
        raise AuthenticationNotFound(AUTHENTICATION_NOT_FOUND)

    return BoundToken(token, user_id)


async def token_dependency(request: Request) -> UUID:
    bound_token = await bound_token_dependency(request)

    return bound_token.user_id


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
