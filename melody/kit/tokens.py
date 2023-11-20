from secrets import token_hex
from typing import AsyncIterator, Optional, Type, TypeVar, overload
from uuid import UUID

from attrs import define, field
from pendulum import DateTime, Duration
from typing_extensions import TypedDict as Data

from melody.kit.core import config, redis
from melody.shared.constants import ACCESS_TOKEN, REFRESH_TOKEN, STAR, VERIFICATION_TOKEN
from melody.shared.converter import CONVERTER
from melody.shared.date_time import utc_now

__all__ = (
    "Tokens",
    "TokensData",
    "access_token_factory",
    "access_expires_in_factory",
    "token_type_factory",
    "refresh_token_factory",
    "refresh_expires_in_factory",
    "verification_token_factory",
    "verification_expires_in_factory",
    "tokens_from_data",
    "tokens_into_data",
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


class TokensData(Data):
    access_token: str
    token_type: str
    refresh_token: str
    created_at: str
    access_expires_in: float
    refresh_expires_in: float


def access_token_factory() -> str:
    return token_hex(config.token.access.size)


def access_expires_in_factory() -> Duration:
    return config.token.access.expires.duration


def token_type_factory() -> str:
    return config.token.type


def refresh_token_factory() -> str:
    return token_hex(config.token.refresh.size)


def refresh_expires_in_factory() -> Duration:
    return config.token.refresh.expires.duration


def verification_token_factory() -> str:
    return token_hex(config.token.verification.size)


def verification_expires_in_factory() -> Duration:
    return config.token.verification.expires.duration


T = TypeVar("T", bound="Tokens")


@define()
class Tokens:
    access_token: str = field(factory=access_token_factory)
    token_type: str = field(factory=token_type_factory)
    refresh_token: str = field(factory=refresh_token_factory)
    created_at: DateTime = field(factory=utc_now)
    access_expires_in: Duration = field()
    refresh_expires_in: Duration = field()

    @access_expires_in.default
    def default_access_expires_in(self) -> Duration:
        return access_expires_in_factory()

    @refresh_expires_in.default
    def default_refresh_expires_in(self) -> Duration:
        return refresh_expires_in_factory()

    @property
    def access_expires_at(self) -> DateTime:
        return self.created_at + self.access_expires_in  # type: ignore

    @property
    def refresh_expires_at(self) -> DateTime:
        return self.created_at + self.refresh_expires_in  # type: ignore

    @classmethod
    def from_data(cls: Type[T], data: TokensData) -> T:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> TokensData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def tokens_from_data(data: TokensData) -> Tokens:
    ...


@overload
def tokens_from_data(data: TokensData, tokens_type: Type[T]) -> T:
    ...


def tokens_from_data(data: TokensData, tokens_type: Type[Tokens] = Tokens) -> Tokens:
    return tokens_type.from_data(data)


def tokens_into_data(tokens: Tokens) -> TokensData:
    return tokens.into_data()


NAME_SEPARATOR = ":"

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


async def generate_tokens_for(user_id: UUID) -> Tokens:
    tokens = Tokens()

    access_expires_seconds = tokens.access_expires_in.total_seconds()  # type: ignore
    refresh_expires_seconds = tokens.refresh_expires_in.total_seconds()  # type: ignore

    await redis.set(
        access_token_key(tokens.access_token), str(user_id), ex=int(access_expires_seconds)
    )
    await redis.set(
        refresh_token_key(tokens.refresh_token), str(user_id), ex=int(refresh_expires_seconds)
    )

    return tokens


async def generate_verification_token_for(user_id: UUID) -> str:
    verification_token = verification_token_factory()

    verification_expires_seconds = verification_expires_in_factory().total_seconds()  # type: ignore

    await redis.set(
        verification_token_key(verification_token),
        str(user_id),
        ex=int(verification_expires_seconds),
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

    if option is None:
        return None

    user_id = UUID(option)

    return user_id


async def fetch_user_id_by_refresh_token(refresh_token: str) -> Optional[UUID]:
    option = await redis.get(refresh_token_key(refresh_token))

    if option is None:
        return None

    user_id = UUID(option)

    return user_id


async def fetch_user_id_by_verification_token(verification_token: str) -> Optional[UUID]:
    option = await redis.get(verification_token_key(verification_token))

    if option is None:
        return None

    user_id = UUID(option)

    return user_id


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
