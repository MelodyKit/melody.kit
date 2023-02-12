from secrets import token_hex
from typing import Optional, Type, TypeVar, overload
from uuid import UUID

from attrs import define, field
from pendulum import DateTime, duration, parse
from typing_extensions import TypedDict as Data

from melody.kit.core import config, redis
from melody.shared.converter import CONVERTER
from melody.shared.date_time import utc_now

__all__ = ("Token", "TokenData", "token_factory", "token_from_data", "token_into_data")


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

    @expires_at.default
    def default_expires_at(self) -> Optional[DateTime]:
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

        if not expires_in.total_seconds():  # type: ignore
            return None

        return self.created_at + expires_in  # type: ignore

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


TOKEN_KEY = "token:{token}"
token_key = TOKEN_KEY.format

EXPIRES_AT_KEY = "expires_at:{token}"
expires_at_key = EXPIRES_AT_KEY.format


async def generate_token(user_id: UUID) -> Token:
    result = Token()

    token = result.token

    await redis.set(token_key(token=token), str(user_id))

    expires_at = result.expires_at

    if expires_at is not None:
        await redis.set(expires_at_key(token=token), str(expires_at))

    return result


CAN_NOT_FIND_TOKEN = "can not find token `{}`"
can_not_find_token = CAN_NOT_FIND_TOKEN.format

EXPIRED_TOKEN = "token `{}` has expired"
expired_token = EXPIRED_TOKEN.format


async def fetch_token(token: str) -> UUID:
    option = await redis.get(token_key(token=token))

    if option is None:
        raise LookupError(can_not_find_token(token))

    user_id = UUID(option)

    option = await redis.get(expires_at_key(token=token))

    if option is None:
        return user_id

    expires_at: DateTime = parse(option)  # type: ignore

    if expires_at > utc_now():
        return user_id

    raise TimeoutError(expired_token(token))
