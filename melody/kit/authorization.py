from secrets import token_urlsafe as token_url_safe
from typing import AsyncIterator, Optional
from uuid import UUID

from attrs import frozen
from fastapi import Depends, Form
from pendulum import Duration
from typing_extensions import Annotated, Self
from melody.kit.contexts import ClientUserContext

from melody.kit.core import config, redis
from melody.kit.errors import AuthError
from melody.shared.constants import AUTHORIZATION_CODE, NAME_SEPARATOR, STAR
from melody.shared.converter import CONVERTER
from melody.shared.tokens import (
    Scopes,
    register_structure_hook_rename_scopes,
    register_unstructure_hook_rename_scopes,
)
from melody.shared.typing import Data

__all__ = (
    "AuthorizationContext",
    "BoundAuthorizationCode",
    "authorization_code_factory",
    "authorization_expires_in_factory",
    "generate_authorization_code_with",
    "delete_authorization_code",
    "delete_authorization_codes_with",
    "fetch_context_by_authorization_code",
    "fetch_authorization_codes_with",
    "bound_authorization_code_dependency",
    "authorization_code_dependency",
    "optional_authorization_code_dependency",
)


class AuthorizationContextData(Data):
    client_id: str
    user_id: str
    scope: str


@register_unstructure_hook_rename_scopes
@register_structure_hook_rename_scopes
@frozen()
class AuthorizationContext:
    client_id: UUID
    user_id: UUID
    scopes: Scopes

    @classmethod
    def from_data(cls, data: AuthorizationContextData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> AuthorizationContextData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]

    def into_context(self) -> ClientUserContext:
        return ClientUserContext(self.client_id, self.user_id, self.scopes)


@frozen()
class BoundAuthorizationCode:
    code: str
    context: AuthorizationContext


def authorization_code_factory() -> str:
    return token_url_safe(config.authorization.size)


def authorization_expires_in_factory() -> Duration:
    return config.authorization.expires.duration


AUTHORIZATION_CODE_KEY = f"{AUTHORIZATION_CODE}{NAME_SEPARATOR}{{}}"
authorization_code_key = AUTHORIZATION_CODE_KEY.format


def key_authorization_code(key: str) -> Optional[str]:
    _, _, authorization_code = key.partition(NAME_SEPARATOR)

    return authorization_code if authorization_code else None


async def generate_authorization_code_with(context: AuthorizationContext) -> str:
    authorization_code = authorization_code_factory()

    authorization_expires = int(authorization_expires_in_factory().total_seconds())

    authorization_code_key_string = authorization_code_key(authorization_code)

    data = context.into_data()

    await redis.hset(authorization_code_key_string, mapping=data)  # type: ignore[arg-type]

    if authorization_expires:
        await redis.expire(authorization_code_key_string, authorization_expires)

    return authorization_code


async def delete_authorization_code(authorization_code: str) -> None:
    await redis.delete(authorization_code_key(authorization_code))


async def delete_authorization_codes_with(context: AuthorizationContext) -> None:
    async for authorization_code in fetch_authorization_codes_with(context):
        await delete_authorization_code(authorization_code)


async def fetch_context_by_authorization_code(
    authorization_code: str,
) -> Optional[AuthorizationContext]:
    data = await redis.hgetall(authorization_code_key(authorization_code))

    return AuthorizationContext.from_data(data) if data else None  # type: ignore[arg-type]


async def fetch_authorization_codes_with(context: AuthorizationContext) -> AsyncIterator[str]:
    async for key in redis.scan_iter(authorization_code_key(STAR)):
        authorization_code = key_authorization_code(key)

        if authorization_code is None:
            continue

        fetched = await fetch_context_by_authorization_code(authorization_code)

        if fetched is None:
            continue

        if fetched == context:
            yield authorization_code


INVALID_AUTHORIZATION_CODE = "authorization code `{}` is invalid"
invalid_authorization_code = INVALID_AUTHORIZATION_CODE.format


FormCodeDependency = Annotated[str, Form()]
OptionalFormCodeDependency = Annotated[Optional[str], Form()]


async def bound_authorization_code_dependency(code: FormCodeDependency) -> BoundAuthorizationCode:
    context = await fetch_context_by_authorization_code(code)

    if context is None:
        raise AuthError(invalid_authorization_code(code))

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
