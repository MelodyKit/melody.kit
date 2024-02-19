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
    client_id: str
    user_id: str
    scope: str


@register_unstructure_hook_rename_scopes
@register_structure_hook_rename_scopes
@frozen()
class AuthorizationContext:
    client_id: UUID
    user_id: UUID
    scopes: Scopes

    @classmethod
    def from_data(cls, data: AuthorizationContextData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> AuthorizationContextData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]

    def into_context(self) -> ClientUserContext:
        return ClientUserContext(self.client_id, self.user_id, self.scopes)
