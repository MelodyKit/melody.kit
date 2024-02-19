from typing import AsyncIterator, Optional

from melody.kit.core import redis
from melody.kit.tokens.context import Context, context_from_data, context_into_data
from melody.kit.tokens.core import Tokens
from melody.kit.tokens.factories import refresh_expires_in_factory
from melody.kit.tokens.keys import (
    access_token_key,
    key_access_token,
    key_refresh_token,
    refresh_token_key,
)
from melody.shared.constants import STAR
from melody.shared.date_time import unstructure_duration

__all__ = (
    "generate_tokens_with",
    "delete_access_token",
    "delete_refresh_token",
    "fetch_context_by_access_token",
    "fetch_context_by_refresh_token",
    "delete_access_tokens_with",
    "delete_refresh_tokens_with",
    "fetch_access_tokens_with",
    "fetch_refresh_tokens_with",
)


async def generate_tokens_with(context: Context) -> Tokens:
    tokens = Tokens()

    expires = unstructure_duration(tokens.expires_in)
    refresh_expires = unstructure_duration(refresh_expires_in_factory())

    data = context_into_data(context)

    access_token_key_string = access_token_key(tokens.access_token)
    refresh_token_key_string = refresh_token_key(tokens.refresh_token)

    await redis.hset(access_token_key_string, mapping=data)  # type: ignore[arg-type]
    await redis.hset(refresh_token_key_string, mapping=data)  # type: ignore[arg-type]

    if expires:
        await redis.expire(access_token_key_string, expires)

    if refresh_expires:
        await redis.expire(refresh_token_key_string, refresh_expires)

    return tokens


async def delete_access_token(access_token: str) -> None:
    await redis.delete(access_token_key(access_token))


async def delete_refresh_token(refresh_token: str) -> None:
    await redis.delete(refresh_token_key(refresh_token))


async def fetch_context_by_access_token(access_token: str) -> Optional[Context]:
    data = await redis.hgetall(access_token_key(access_token))

    return context_from_data(data) if data else None  # type: ignore[arg-type]


async def fetch_context_by_refresh_token(refresh_token: str) -> Optional[Context]:
    data = await redis.hgetall(refresh_token_key(refresh_token))

    return context_from_data(data) if data else None  # type: ignore[arg-type]


async def delete_access_tokens_with(context: Context) -> None:
    async for access_token in fetch_access_tokens_with(context):
        await delete_access_token(access_token)


async def delete_refresh_tokens_with(context: Context) -> None:
    async for refresh_token in fetch_refresh_tokens_with(context):
        await delete_refresh_token(refresh_token)


async def fetch_access_tokens_with(context: Context) -> AsyncIterator[str]:
    async for key in redis.scan_iter(access_token_key(STAR)):
        access_token = key_access_token(key)

        if access_token is None:
            continue

        fetched = await fetch_context_by_access_token(access_token)

        if fetched is None:
            continue

        if fetched == context:
            yield access_token


async def fetch_refresh_tokens_with(context: Context) -> AsyncIterator[str]:
    async for key in redis.scan_iter(refresh_token_key(STAR)):
        refresh_token = key_refresh_token(key)

        if refresh_token is None:
            continue

        fetched = await fetch_context_by_refresh_token(refresh_token)

        if fetched is None:
            continue

        if fetched == context:
            yield refresh_token
