from typing import Type, TypeVar, overload

from attrs import define, field
from cattrs.gen import make_dict_structure_fn, make_dict_unstructure_fn, override
from pendulum import DateTime

from melody.shared.converter import CONVERTER
from melody.shared.date_time import utc_now
from melody.spotify.models.base import Base, BaseData


class TokensData(BaseData):
    access_token: str
    token_type: str
    expires_in: int


T = TypeVar("T", bound="Tokens")


@define()
class Tokens(Base):
    token: str = field()
    type: str = field()
    expires_seconds: int = field()

    created_at: DateTime = field(factory=utc_now)

    @property
    def expires_at(self) -> DateTime:
        return self.created_at.add(seconds=self.expires_seconds)

    @classmethod
    def from_data(cls: Type[T], data: TokensData) -> T:  # type: ignore
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


ACCESS_TOKEN = "access_token"
TOKEN_TYPE = "token_type"
EXPIRES_IN = "expires_in"


CONVERTER.register_unstructure_hook(
    Tokens,
    make_dict_unstructure_fn(
        Tokens,
        CONVERTER,
        token=override(rename=ACCESS_TOKEN),
        type=override(rename=TOKEN_TYPE),
        expires_seconds=override(rename=EXPIRES_IN),
        created_at=override(omit=True),
    ),
)

CONVERTER.register_structure_hook(
    Tokens,
    make_dict_structure_fn(
        Tokens,
        CONVERTER,
        token=override(rename=ACCESS_TOKEN),
        type=override(rename=TOKEN_TYPE),
        expires_seconds=override(rename=EXPIRES_IN),
    ),
)
