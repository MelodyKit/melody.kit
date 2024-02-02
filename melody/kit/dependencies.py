from typing import Optional, Set
from uuid import UUID

from async_extensions import run_blocking_in_thread
from email_validator import EmailNotValidError, validate_email
from fastapi import Body
from fastapi.requests import Request
from iters.iters import iter
from yarl import URL

from melody.kit.enums import EntityType
from melody.kit.errors import AuthInvalid, ValidationError
from melody.kit.tokens import BoundToken, fetch_user_id_by_verification_token

__all__ = (
    "bound_verification_token_dependency",
    "verification_token_dependency",
    "email_dependency",
    "email_deliverability_dependency",
    "request_url_dependency",
    "types_dependency",
)

AUTHENTICATION_INVALID = "authentication is invalid"


async def bound_verification_token_dependency(verification_token: str = Body()) -> BoundToken:
    self_id = await fetch_user_id_by_verification_token(verification_token)

    if self_id is None:
        raise AuthInvalid(AUTHENTICATION_INVALID)

    return BoundToken(verification_token, self_id)


async def verification_token_dependency(verification_token: str = Body()) -> UUID:
    bound_token = await bound_verification_token_dependency(verification_token)

    return bound_token.self_id


INVALID_EMAIL = "email `{}` is invalid"
invalid_email = INVALID_EMAIL.format


def email_dependency(email: str = Body()) -> str:
    try:
        result = validate_email(email, check_deliverability=False)

    except EmailNotValidError:
        raise ValidationError(invalid_email(email)) from None

    return result.email  # type: ignore[no-any-return]


async def email_deliverability_dependency(email: str = Body()) -> str:
    try:
        result = await run_blocking_in_thread(validate_email, email, check_deliverability=True)

    except EmailNotValidError:
        raise ValidationError(invalid_email(email)) from None

    return result.email  # type: ignore[no-any-return]


def request_url_dependency(request: Request) -> URL:
    return URL(str(request.url))


INVALID_TYPES = "types `{}` are invalid"
invalid_types = INVALID_TYPES.format

TYPES_SEPARATOR = ","


def types_dependency(types: Optional[str] = None) -> Set[EntityType]:
    if types is None:
        return set(EntityType)

    try:
        return iter(types.split(TYPES_SEPARATOR)).map(EntityType).set()

    except ValueError:
        raise ValidationError(invalid_types(types)) from None
