from typing import AsyncIterator, Optional

from melody.kit.authorization.context import AuthorizationContext
from melody.kit.authorization.factories import (
    authorization_code_factory,
    authorization_expires_in_factory,
)
from melody.kit.authorization.keys import authorization_code_key, key_authorization_code
from melody.kit.core import redis
from melody.shared.constants import STAR
from melody.shared.date_time import unstructure_duration

__all__ = (
    "generate_authorization_code_with",
    "delete_authorization_code",
    "delete_authorization_codes_with",
    "fetch_context_by_authorization_code",
    "fetch_authorization_codes_with",
)


async def generate_authorization_code_with(context: AuthorizationContext) -> str:
    authorization_code = authorization_code_factory()

    authorization_expires = unstructure_duration(authorization_expires_in_factory())

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
