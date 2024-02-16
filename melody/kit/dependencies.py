from typing import Optional, Set

from async_extensions import run_blocking_in_thread
from email_validator import EmailNotValidError, validate_email
from fastapi import Depends, File, Form, Query, UploadFile
from fastapi.requests import Request
from iters.iters import iter
from typing_extensions import Annotated
from yarl import URL

from melody.kit.constants import MAX_LIMIT, MIN_LIMIT, MIN_OFFSET
from melody.kit.enums import EntityType
from melody.kit.errors import ValidationError

__all__ = (
    # common
    "OffsetDependency",
    "LimitDependency",
    "FileDependency",
    # emails
    "EmailDependency",
    "EmailDeliverabilityDependency",
    "email_dependency",
    "email_deliverability_dependency",
    # request URLs
    "RequestURLDependency",
    "request_url_dependency",
    # types
    "TypesDependency",
    "types_dependency",
)


INVALID_EMAIL = "email `{}` is invalid"
invalid_email = INVALID_EMAIL.format


FormEmailDependency = Annotated[str, Form()]


def email_dependency(email: FormEmailDependency) -> str:
    try:
        result = validate_email(email, check_deliverability=False)

    except EmailNotValidError:
        raise ValidationError(invalid_email(email)) from None

    return result.normalized


EmailDependency = Annotated[str, Depends(email_dependency)]


async def email_deliverability_dependency(email: FormEmailDependency) -> str:
    try:
        result = await run_blocking_in_thread(validate_email, email, check_deliverability=True)

    except EmailNotValidError:
        raise ValidationError(invalid_email(email)) from None

    return result.normalized


EmailDeliverabilityDependency = Annotated[str, Depends(email_deliverability_dependency)]


def request_url_dependency(request: Request) -> URL:
    return URL(str(request.url))


RequestURLDependency = Annotated[URL, Depends(request_url_dependency)]


INVALID_TYPES = "types `{}` are invalid"
invalid_types = INVALID_TYPES.format

TYPES_SEPARATOR = ","

EntityTypes = Set[EntityType]


def split_types(types: str) -> Set[str]:
    if not types:
        return set()

    return set(types.split(TYPES_SEPARATOR))


def types_dependency(types: Optional[str] = None) -> EntityTypes:
    if types is None:
        return set(EntityType)

    try:
        return iter(split_types(types)).map(EntityType).set()

    except ValueError:
        raise ValidationError(invalid_types(types)) from None


TypesDependency = Annotated[EntityTypes, Depends(types_dependency)]


# common dependencies

OffsetDependency = Annotated[int, Query(ge=MIN_OFFSET)]
LimitDependency = Annotated[int, Query(ge=MIN_LIMIT, le=MAX_LIMIT)]

FileDependency = Annotated[UploadFile, File()]
