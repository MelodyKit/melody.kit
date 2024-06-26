from typing import FrozenSet, Iterable, List, Optional, Type, TypeVar

from attrs import Factory, frozen
from cattrs.gen import override
from pendulum import DateTime, Duration
from typing_extensions import Self

from melody.shared.converter import (
    CONVERTER,
    register_structure_hook,
    register_unstructure_hook,
)
from melody.shared.time import unstructure_duration, utc_now
from melody.shared.typing import Data

__all__ = ("Scopes", "TokensData", "Tokens", "AuthorizationData", "authorization")

SCOPE_SEPARATOR = " "
concat_scopes = SCOPE_SEPARATOR.join


def split_scope(scope: str) -> List[str]:
    if not scope:
        return []

    return scope.split(SCOPE_SEPARATOR)


def converter(tokens: Iterable[str]) -> FrozenSet[str]:
    return frozenset(tokens)


S = TypeVar("S", bound="Scopes")


@frozen()
class Scopes:
    tokens: FrozenSet[str] = Factory(frozenset)

    @classmethod
    def from_scope(cls, scope: str) -> Self:
        return cls.from_iterable(split_scope(scope))

    @classmethod
    def from_iterable(cls, iterable: Iterable[str]) -> Self:
        return cls(frozenset(iterable))

    def to_scope(self) -> str:
        return concat_scopes(self.tokens)

    @property
    def scope(self) -> str:
        return self.to_scope()

    def has_tokens(self, tokens: Iterable[str]) -> bool:
        return frozenset(tokens) <= self.tokens

    def has(self, *tokens: str) -> bool:
        return self.has_tokens(tokens)


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


register_unstructure_hook_rename_scopes = register_unstructure_hook(scopes=override(rename=SCOPE))
register_structure_hook_rename_scopes = register_structure_hook(scopes=override(rename=SCOPE))


@register_unstructure_hook_rename_scopes
@register_structure_hook_rename_scopes
@frozen()
class Tokens:
    access_token: str
    refresh_token: str

    token_type: str

    expires_in: Duration

    scopes: Scopes = Factory(Scopes)

    created_at: DateTime = Factory(utc_now)

    @property
    def expires_at(self) -> Optional[DateTime]:
        # `expires_in` of `0` means no expiration

        expires_in = self.expires_in

        if unstructure_duration(expires_in):
            return self.created_at + expires_in

        return None

    @classmethod
    def from_data(cls, data: TokensData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> TokensData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


AUTHORIZATION = "Authorization"
AUTHORIZATION_SEPARATOR = " "

AUTHORIZATION_FORMAT = "{type} {content}"
authorization_format = AUTHORIZATION_FORMAT.format


class AuthorizationData(Data):
    Authorization: str


def authorization(tokens: Tokens) -> AuthorizationData:
    return AuthorizationData(
        Authorization=authorization_format(type=tokens.token_type, content=tokens.access_token)
    )
