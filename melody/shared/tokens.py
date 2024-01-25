from typing import List, Type, TypeVar
from attrs import define, field
from cattrs.gen import override
from pendulum import DateTime
from typing_extensions import Self

from melody.shared.converter import (
    CONVERTER,
    register_structure_hook,
    register_unstructure_hook,
)
from melody.shared.date_time import utc_now
from melody.shared.typing import Data

__all__ = ("Scopes", "TokensData", "Tokens")

SCOPE_SEPARATOR = " "
concat_scopes = SCOPE_SEPARATOR.join


def split_scope(scope: str) -> List[str]:
    return scope.split(SCOPE_SEPARATOR)


S = TypeVar("S", bound="Scopes")


@define()
class Scopes:
    scopes: List[str] = field(factory=list)

    @classmethod
    def from_scope(cls, scope: str) -> Self:
        return cls(split_scope(scope))

    def to_scope(self) -> str:
        return concat_scopes(self.scopes)

    @property
    def scope(self) -> str:
        return self.to_scope()


def structure_scopes(scope: str, scopes_type: Type[S]) -> S:
    return scopes_type.from_scope(scope)


def unstructure_scopes(scopes: Scopes) -> str:
    return scopes.to_scope()


CONVERTER.register_structure_hook(Scopes, structure_scopes)
CONVERTER.register_unstructure_hook(Scopes, unstructure_scopes)


class TokensData(Data):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    scope: str


ACCESS_TOKEN = "access_token"
REFRESH_TOKEN = "refresh_token"
TOKEN_TYPE = "token_type"
EXPIRES_IN = "expires_in"
SCOPE = "scope"


register_unstructure_hook_tokens = register_unstructure_hook(
    token=override(rename=ACCESS_TOKEN),
    type=override(rename=TOKEN_TYPE),
    expires_seconds=override(rename=EXPIRES_IN),
    scopes=override(rename=SCOPE),
    created_at=override(omit=True),
)

register_structure_hook_tokens = register_structure_hook(
    token=override(rename=ACCESS_TOKEN),
    type=override(rename=TOKEN_TYPE),
    expires_seconds=override(rename=EXPIRES_IN),
    scopes=override(rename=SCOPE),
)


@register_unstructure_hook_tokens
@register_structure_hook_tokens
@define()
class Tokens:
    token: str = field()
    refresh_token: str = field()

    type: str = field()
    expires_seconds: int = field()

    scopes: Scopes = field(factory=Scopes)

    created_at: DateTime = field(factory=utc_now)

    @property
    def expires_at(self) -> DateTime:
        return self.created_at.add(seconds=self.expires_seconds)

    @classmethod
    def from_data(cls, data: TokensData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> TokensData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]
