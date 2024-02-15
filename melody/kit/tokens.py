from secrets import token_hex
from typing import AsyncIterator, Optional

from attrs import define, field
from pendulum import Duration

from melody.kit.contexts import Context, context_from_data, context_into_data
from melody.kit.core import config, redis
from melody.shared.constants import ACCESS_TOKEN, NAME_SEPARATOR, REFRESH_TOKEN, STAR
from melody.shared.tokens import Tokens as SharedTokens

__all__ = (
    # tokens with factories
    "Tokens",
    # factories
    "access_token_factory",
    "expires_in_factory",
    "token_type_factory",
    "refresh_token_factory",
    "refresh_expires_in_factory",
    # keys
    "access_token_key",
    "refresh_token_key",
    "key_access_token",
    "key_refresh_token",
    # tokens
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


def access_token_factory() -> str:
    return token_hex(config.token.access.size)


def expires_in_factory() -> Duration:
    return config.token.access.expires.duration


def token_type_factory() -> str:
    return config.token.type


def refresh_token_factory() -> str:
    return token_hex(config.token.refresh.size)


def refresh_expires_in_factory() -> Duration:
    return config.token.refresh.expires.duration


@define()
class Tokens(SharedTokens):
    # NOTE: here we simply provide defaults to fields in `melody.shared` without them

    access_token: str = field(factory=access_token_factory)
    expires_in: Duration = field(factory=expires_in_factory)
    token_type: str = field(factory=token_type_factory)
    refresh_token: str = field(factory=refresh_token_factory)


ACCESS_TOKEN_KEY = f"{ACCESS_TOKEN}{NAME_SEPARATOR}{{}}"
access_token_key = ACCESS_TOKEN_KEY.format

REFRESH_TOKEN_KEY = f"{REFRESH_TOKEN}{NAME_SEPARATOR}{{}}"
refresh_token_key = REFRESH_TOKEN_KEY.format


def key_access_token(key: str) -> Optional[str]:
    _, _, access_token = key.partition(NAME_SEPARATOR)

    return access_token if access_token else None


def key_refresh_token(key: str) -> Optional[str]:
    _, _, refresh_token = key.partition(NAME_SEPARATOR)

    return refresh_token if refresh_token else None


async def generate_tokens_with(context: Context) -> Tokens:
    tokens = Tokens()

    expires = int(tokens.expires_in.total_seconds())
    refresh_expires = int(refresh_expires_in_factory().total_seconds())

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
