from attrs import frozen
from typing_extensions import Self

from melody.shared.converter import CONVERTER
from melody.shared.typing import Data

__all__ = ("AuthorizationCode", "AuthorizationCodeData")


class AuthorizationCodeData(Data):
    code: str
    state: str


@frozen()
class AuthorizationCode:
    code: str
    state: str

    @classmethod
    def from_data(cls, data: AuthorizationCodeData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> AuthorizationCodeData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]
