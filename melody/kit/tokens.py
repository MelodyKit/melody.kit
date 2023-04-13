from secrets import token_hex
from typing import AsyncIterator, Optional, Type, TypeVar, overload
from uuid import UUID

from attrs import define, field
from pendulum import DateTime, Duration, duration
from typing_extensions import TypedDict as Data

from melody.kit.core import config, redis
from melody.shared.constants import STAR, TOKEN, VERIFICATION_TOKEN
from melody.shared.converter import CONVERTER
from melody.shared.date_time import utc_now

__all__ = (
    "Token",
    "TokenData",
    "token_factory",
    "token_from_data",
    "token_into_data",
    "generate_token_for",
    "generate_verification_token_for",
    "delete_token",
    "delete_verification_token",
    "delete_tokens_for",
    "delete_verification_tokens_for",
    "fetch_user_id_by",
    "fetch_user_id_by_verification",
    "fetch_tokens_for",
    "fetch_verification_tokens_for",
)


class TokenData(Data):
    token: str
    token_type: str
    created_at: DateTime
    expires_at: Optional[DateTime]


def token_factory() -> str:
    return token_hex(config.token.size)


def token_type_factory() -> str:
    return config.token.type


T = TypeVar("T", bound="Token")


@define()
class Token:
    token: str = field(factory=token_factory)
    token_type: str = field(factory=token_type_factory)
    created_at: DateTime = field(factory=utc_now)
    expires_at: Optional[DateTime] = field()

    def __str__(self) -> str:
        return self.token

    @expires_at.default
    def default_expires_at(self) -> Optional[DateTime]:
        expires_in = self.expires_in

        return None if expires_in is None else self.created_at + expires_in

    @property
    def expires_in(self) -> Optional[Duration]:
        expires = config.token.expires

        expires_in = duration(
            years=expires.years,
            months=expires.months,
            weeks=expires.weeks,
            days=expires.days,
            hours=expires.hours,
            minutes=expires.minutes,
            seconds=expires.seconds,
        )

        return expires_in if expires_in.total_seconds() else None  # type: ignore

    @classmethod
    def from_data(cls: Type[T], data: TokenData) -> T:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> TokenData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def token_from_data(data: TokenData) -> Token:
    ...


@overload
def token_from_data(data: TokenData, token_type: Type[T]) -> T:
    ...


def token_from_data(data: TokenData, token_type: Type[Token] = Token) -> Token:
    return token_type.from_data(data)


def token_into_data(token: Token) -> TokenData:
    return token.into_data()


NAME_SEPARATOR = ":"

TOKEN_KEY = f"{TOKEN}{NAME_SEPARATOR}{{}}"
token_key = TOKEN_KEY.format

VERIFICATION_TOKEN_KEY = f"{VERIFICATION_TOKEN}{NAME_SEPARATOR}{{}}"
verification_token_key = VERIFICATION_TOKEN_KEY.format


def key_token(key: str) -> Optional[str]:
    _, _, token = key.partition(NAME_SEPARATOR)

    return token if token else None


def key_verification_token(key: str) -> Optional[str]:
    _, _, verification_token = key.partition(NAME_SEPARATOR)

    return verification_token if verification_token else None


async def generate_token_for(user_id: UUID) -> Token:
    token = Token()

    expires_in = token.expires_in

    expires_seconds = None if expires_in is None else expires_in.total_seconds()  # type: ignore

    await redis.set(token_key(token), str(user_id), ex=expires_seconds)

    return token


async def generate_verification_token_for(user_id: UUID) -> str:
    verification_token = token_factory()

    await redis.set(verification_token_key(verification_token), str(user_id))

    return verification_token


async def delete_token(token: str) -> None:
    await redis.delete(token_key(token))


async def delete_verification_token(verification_token: str) -> None:
    await redis.delete(verification_token_key(verification_token))


async def delete_tokens_for(user_id: UUID) -> None:
    async for token in fetch_tokens_for(user_id):
        await delete_token(token)


async def delete_verification_tokens_for(user_id: UUID) -> None:
    async for verification_token in fetch_verification_tokens_for(user_id):
        await delete_verification_token(verification_token)


async def fetch_user_id_by(token: str) -> Optional[UUID]:
    option = await redis.get(token_key(token))

    if option is None:
        return None

    user_id = UUID(option)

    return user_id


async def fetch_user_id_by_verification(verification_token: str) -> Optional[UUID]:
    option = await redis.get(verification_token_key(verification_token_key))

    if option is None:
        return None

    user_id = UUID(option)

    return user_id


async def fetch_tokens_for(user_id: UUID) -> AsyncIterator[str]:
    async for key in redis.scan_iter(token_key(STAR)):
        option = await redis.get(key)

        if option is None:
            continue

        target_id = UUID(option)

        if target_id == user_id:
            token = key_token(key)

            if token is None:
                continue

            yield token


async def fetch_verification_tokens_for(user_id: UUID) -> AsyncIterator[str]:
    async for key in redis.scan_iter(verification_token_key(STAR)):
        option = await redis.get(key)

        if option is None:
            continue

        target_id = UUID(option)

        if target_id == user_id:
            token = key_verification_token(key)

            if token is None:
                continue

            yield token
