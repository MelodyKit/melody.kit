from async_extensions import run_blocking_in_thread
from email_validator import EmailNotValidError, validate_email
from fastapi import Depends, Form
from typing_extensions import Annotated

from melody.kit.errors.auth import AuthEmailInvalid

__all__ = (
    # dependencies
    "EmailDependency",
    "EmailDeliverabilityDependency",
    # dependables
    "email_dependency",
    "email_deliverability_dependency",
)


INVALID_EMAIL = "email `{}` is invalid"
invalid_email = INVALID_EMAIL.format


FormEmailDependency = Annotated[str, Form()]


def email_dependency(email: FormEmailDependency) -> str:
    try:
        result = validate_email(email, check_deliverability=False)

    except EmailNotValidError:
        raise AuthEmailInvalid(email) from None

    return result.normalized


EmailDependency = Annotated[str, Depends(email_dependency)]


async def email_deliverability_dependency(email: FormEmailDependency) -> str:
    try:
        result = await run_blocking_in_thread(validate_email, email, check_deliverability=True)

    except EmailNotValidError:
        raise AuthEmailInvalid(email) from None

    return result.normalized


EmailDeliverabilityDependency = Annotated[str, Depends(email_deliverability_dependency)]
