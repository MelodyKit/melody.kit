from typing import Optional

from attrs import frozen
from fastapi import Depends, Form
from typing_extensions import Annotated

from melody.kit.authorization.context import AuthorizationContext
from melody.kit.authorization.operations import fetch_context_by_authorization_code
from melody.kit.errors.auth import AuthAuthorizationCodeInvalid

__all__ = (
    # types
    "BoundAuthorizationCode",
    # dependencies
    "BoundAuthorizationCodeDependency",
    "AuthorizationCodeDependency",
    "OptionalAuthorizationCodeDependency",
    # dependables
    "bound_authorization_code_dependency",
    "authorization_code_dependency",
    "optional_authorization_code_dependency",
)


@frozen()
class BoundAuthorizationCode:
    code: str
    context: AuthorizationContext


FormCodeDependency = Annotated[str, Form()]
OptionalFormCodeDependency = Annotated[Optional[str], Form()]


async def bound_authorization_code_dependency(code: FormCodeDependency) -> BoundAuthorizationCode:
    context = await fetch_context_by_authorization_code(code)

    if context is None:
        raise AuthAuthorizationCodeInvalid()

    return BoundAuthorizationCode(code, context)


BoundAuthorizationCodeDependency = Annotated[
    BoundAuthorizationCode, Depends(bound_authorization_code_dependency)
]


async def authorization_code_dependency(code: FormCodeDependency) -> AuthorizationContext:
    bound_authorization_code = await bound_authorization_code_dependency(code)

    return bound_authorization_code.context


AuthorizationCodeDependency = Annotated[
    AuthorizationContext, Depends(authorization_code_dependency)
]


async def optional_authorization_code_dependency(
    code: OptionalFormCodeDependency = None,
) -> Optional[AuthorizationContext]:
    return None if code is None else await authorization_code_dependency(code)


OptionalAuthorizationCodeDependency = Annotated[
    Optional[AuthorizationContext], Depends(optional_authorization_code_dependency)
]
