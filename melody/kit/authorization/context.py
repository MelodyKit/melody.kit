from uuid import UUID

from attrs import frozen
from typing_extensions import Self

from melody.kit.tokens.context import ClientUserContext
from melody.shared.converter import CONVERTER
from melody.shared.tokens import (
    Scopes,
    register_structure_hook_rename_scopes,
    register_unstructure_hook_rename_scopes,
)
from melody.shared.typing import Data

__all__ = ("AuthorizationContext", "AuthorizationContextData")


class AuthorizationContextData(Data):
    user_id: str
    client_id: str
    scope: str
    redirect_uri: str


@register_unstructure_hook_rename_scopes
@register_structure_hook_rename_scopes
@frozen()
class AuthorizationContext:
    user_id: UUID
    client_id: UUID
    scopes: Scopes
    redirect_uri: str

    @classmethod
    def from_data(cls, data: AuthorizationContextData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> AuthorizationContextData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]

    def into_context(self) -> ClientUserContext:
        return ClientUserContext(self.client_id, self.user_id, self.scopes)
