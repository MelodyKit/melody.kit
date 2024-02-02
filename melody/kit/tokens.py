from secrets import token_hex
from typing import AsyncIterator, Optional
from uuid import UUID

from attrs import define, field, frozen
from pendulum import Duration

from melody.kit.core import config, redis
from melody.shared.constants import (
    ACCESS_TOKEN,
    NAME_SEPARATOR,
    REFRESH_TOKEN,
    STAR,
    VERIFICATION_TOKEN,
)
from melody.shared.tokens import Tokens as SharedTokens

__all__ = (
    "BoundToken",
    "Tokens",
    "access_token_factory",
    "expires_in_factory",
    "token_type_factory",
    "refresh_token_factory",
    "refresh_expires_in_factory",
    "verification_token_factory",
    "verification_expires_in_factory",
    "generate_tokens_for",
    "generate_verification_token_for",
    "delete_access_token",
    "delete_refresh_token",
    "delete_verification_token",
    "delete_access_tokens_for",
    "delete_refresh_tokens_for",
    "delete_verification_tokens_for",
    "fetch_user_id_by_access_token",
    "fetch_user_id_by_refresh_token",
    "fetch_user_id_by_verification_token",
    "fetch_access_tokens_for",
    "fetch_refresh_tokens_for",
    "fetch_verification_tokens_for",
)


@frozen()
class BoundToken:
    token: str
    self_id: UUID


def access_token_factory() -> str:
    return token_hex(config.token.access.size)


def expires_in_factory() -> Duration:
    return config.token.access.expires.duration


def token_type_factory() -> str:
    return config.token.type


def refresh_token_factory() -> str:
    return token_hex(config.token.refresh.size)


def verification_token_factory() -> str:
    return token_hex(config.token.verification.size)


def verification_expires_in_factory() -> Duration:
    return config.token.verification.expires.duration


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

VERIFICATION_TOKEN_KEY = f"{VERIFICATION_TOKEN}{NAME_SEPARATOR}{{}}"
verification_token_key = VERIFICATION_TOKEN_KEY.format


def key_access_token(key: str) -> Optional[str]:
    _, _, access_token = key.partition(NAME_SEPARATOR)

    return access_token if access_token else None


def key_refresh_token(key: str) -> Optional[str]:
    _, _, refresh_token = key.partition(NAME_SEPARATOR)

    return refresh_token if refresh_token else None


def key_verification_token(key: str) -> Optional[str]:
    _, _, verification_token = key.partition(NAME_SEPARATOR)

    return verification_token if verification_token else None


def refresh_expires_in_factory() -> Duration:
    return config.token.refresh.expires.duration


async def generate_tokens_for(user_id: UUID) -> Tokens:
    tokens = Tokens()

    expires = int(tokens.expires_in.total_seconds())
    refresh_expires = int(refresh_expires_in_factory().total_seconds())

    await redis.set(
        access_token_key(tokens.access_token),
        str(user_id),
        ex=expires,
    )
    await redis.set(
        refresh_token_key(tokens.refresh_token),
        str(user_id),
        ex=refresh_expires,
    )

    return tokens


async def generate_verification_token_for(user_id: UUID) -> str:
    verification_token = verification_token_factory()

    verification_expires = int(verification_expires_in_factory().total_seconds())

    await redis.set(
        verification_token_key(verification_token),
        str(user_id),
        ex=verification_expires,
    )

    return verification_token


async def delete_access_token(access_token: str) -> None:
    await redis.delete(access_token_key(access_token))


async def delete_refresh_token(refresh_token: str) -> None:
    await redis.delete(refresh_token_key(refresh_token))


async def delete_verification_token(verification_token: str) -> None:
    await redis.delete(verification_token_key(verification_token))


async def delete_access_tokens_for(user_id: UUID) -> None:
    async for access_token in fetch_access_tokens_for(user_id):
        await delete_access_token(access_token)


async def delete_refresh_tokens_for(user_id: UUID) -> None:
    async for refresh_token in fetch_refresh_tokens_for(user_id):
        await delete_refresh_token(refresh_token)


async def delete_verification_tokens_for(user_id: UUID) -> None:
    async for verification_token in fetch_verification_tokens_for(user_id):
        await delete_verification_token(verification_token)


async def fetch_user_id_by_access_token(access_token: str) -> Optional[UUID]:
    option = await redis.get(access_token_key(access_token))

    return None if option is None else UUID(option)


async def fetch_user_id_by_refresh_token(refresh_token: str) -> Optional[UUID]:
    option = await redis.get(refresh_token_key(refresh_token))

    return None if option is None else UUID(option)


async def fetch_user_id_by_verification_token(
    verification_token: str,
) -> Optional[UUID]:
    option = await redis.get(verification_token_key(verification_token))

    return None if option is None else UUID(option)


async def fetch_access_tokens_for(user_id: UUID) -> AsyncIterator[str]:
    async for key in redis.scan_iter(access_token_key(STAR)):
        option = await redis.get(key)

        if option is None:
            continue

        target_id = UUID(option)

        if target_id == user_id:
            access_token = key_access_token(key)

            if access_token is None:
                continue

            yield access_token


async def fetch_refresh_tokens_for(user_id: UUID) -> AsyncIterator[str]:
    async for key in redis.scan_iter(refresh_token_key(STAR)):
        option = await redis.get(key)

        if option is None:
            continue

        target_id = UUID(option)

        if target_id == user_id:
            refresh_token = key_refresh_token(key)

            if refresh_token is None:
                continue

            yield refresh_token


async def fetch_verification_tokens_for(user_id: UUID) -> AsyncIterator[str]:
    async for key in redis.scan_iter(verification_token_key(STAR)):
        option = await redis.get(key)

        if option is None:
            continue

        target_id = UUID(option)

        if target_id == user_id:
            verification_token = key_verification_token(key)

            if verification_token is None:
                continue

            yield verification_token
