from typing import Type, TypeVar, overload

from attrs import define, field
from cattrs.gen import override
from pendulum import DateTime

from melody.shared.converter import CONVERTER, register_structure_hook, register_unstructure_hook
from melody.shared.date_time import utc_now
from melody.spotify.models.base import Base, BaseData


class TokensData(BaseData):
    access_token: str
    token_type: str
    expires_in: int


ACCESS_TOKEN = "access_token"
TOKEN_TYPE = "token_type"
EXPIRES_IN = "expires_in"

register_unstructure_hook_rename_and_omit = register_unstructure_hook(
    token=override(rename=ACCESS_TOKEN),
    type=override(rename=TOKEN_TYPE),
    expires_seconds=override(rename=EXPIRES_IN),
    created_at=override(omit=True),
)

register_structure_hook_rename = register_structure_hook(
    token=override(rename=ACCESS_TOKEN),
    type=override(rename=TOKEN_TYPE),
    expires_seconds=override(rename=EXPIRES_IN),
)


T = TypeVar("T", bound="Tokens")


@register_unstructure_hook_rename_and_omit
@register_structure_hook_rename
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
