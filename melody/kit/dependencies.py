from typing import Optional, Set
from uuid import UUID

from attrs import define
from email_validator import EmailNotValidError, validate_email
from fastapi import Body
from fastapi.requests import Request
from iters.iters import iter
from yarl import URL
from melody.kit.enums import EntityType

from melody.kit.errors import (
    AuthenticationError,
    AuthenticationInvalid,
    AuthenticationMissing,
    AuthenticationNotFound,
    ValidationError,
)
from melody.kit.tokens import (
    fetch_user_id_by_access_token,
    fetch_user_id_by_refresh_token,
    fetch_user_id_by_verification_token,
)
from melody.shared.asyncio import run_blocking
from melody.shared.constants import SPACE

__all__ = (
    "BoundToken",
    "bound_access_token_dependency",
    "access_token_dependency",
    "optional_access_token_dependency",
    "bound_refresh_token_dependency",
    "refresh_token_dependency",
    "bound_verification_token_dependency",
    "verification_token_dependency",
    "email_dependency",
    "email_deliverability_dependency",
    "url_dependency",
    "types_dependency",
)


@define()
class BoundToken:
    token: str
    user_id: UUID


AUTHORIZATION = "Authorization"

AUTHENTICATION_INVALID = "authentication is invalid"
AUTHENTICATION_MISSING = "authentication is missing"
AUTHENTICATION_NOT_FOUND = "authentication not found"


def simple_token_dependency(request: Request, token: Optional[str] = None) -> str:
    if token is None:
        header = request.headers.get(AUTHORIZATION)

        if header is None:
            raise AuthenticationMissing(AUTHENTICATION_MISSING)

        _, _, token = header.partition(SPACE)

        if not token:
            raise AuthenticationInvalid(AUTHENTICATION_INVALID)

    return token


async def bound_access_token_dependency(
    request: Request, token: Optional[str] = None
) -> BoundToken:
    access_token = simple_token_dependency(request, token)

    user_id = await fetch_user_id_by_access_token(access_token)

    if user_id is None:
        raise AuthenticationNotFound(AUTHENTICATION_NOT_FOUND)

    return BoundToken(access_token, user_id)


async def access_token_dependency(request: Request, token: Optional[str] = None) -> UUID:
    bound_token = await bound_access_token_dependency(request, token)

    return bound_token.user_id


async def bound_refresh_token_dependency(
    request: Request, token: Optional[str] = None
) -> BoundToken:
    refresh_token = simple_token_dependency(request, token)

    user_id = await fetch_user_id_by_refresh_token(refresh_token)

    if user_id is None:
        raise AuthenticationNotFound(AUTHENTICATION_NOT_FOUND)

    return BoundToken(refresh_token, user_id)


async def refresh_token_dependency(request: Request, token: Optional[str] = None) -> UUID:
    bound_token = await bound_refresh_token_dependency(request, token)

    return bound_token.user_id


async def optional_access_token_dependency(
    request: Request, token: Optional[str] = None
) -> Optional[UUID]:
    try:
        return await access_token_dependency(request, token)

    except AuthenticationError:
        return None


async def bound_verification_token_dependency(verification_token: str) -> BoundToken:
    user_id = await fetch_user_id_by_verification_token(verification_token)

    if user_id is None:
        raise AuthenticationNotFound(AUTHENTICATION_NOT_FOUND)

    return BoundToken(verification_token, user_id)


async def verification_token_dependency(verification_token: str) -> UUID:
    bound_token = await bound_verification_token_dependency(verification_token)

    return bound_token.user_id


INVALID_EMAIL = "email `{}` is invalid"


def email_dependency(email: str = Body()) -> str:
    try:
        result = validate_email(email, check_deliverability=False)

    except EmailNotValidError:
        raise ValidationError(INVALID_EMAIL.format(email)) from None

    return result.email  # type: ignore[no-any-return]


async def email_deliverability_dependency(email: str = Body()) -> str:
    try:
        result = await run_blocking(validate_email, email, check_deliverability=True)

    except EmailNotValidError:
        raise ValidationError(INVALID_EMAIL.format(email)) from None

    return result.email  # type: ignore[no-any-return]


def url_dependency(request: Request) -> URL:
    return URL(str(request.url))


INVALID_TYPES = "types `{}` are invalid"
TYPES_SEPARATOR = ","


def types_dependency(types: Optional[str] = None) -> Set[EntityType]:
    if types is None:
        return set(EntityType)

    try:
        return iter(types.split(TYPES_SEPARATOR)).map(EntityType).set()

    except ValueError:
        raise ValidationError(INVALID_TYPES.format(types)) from None
