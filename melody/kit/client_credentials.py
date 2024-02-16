from uuid import UUID

from attrs import frozen
from typing_extensions import Self

from melody.shared.converter import CONVERTER
from melody.shared.typing import Data

__all__ = ("ClientCredentials", "ClientCredentialsData")


class ClientCredentialsData(Data):
    id: str
    secret: str


@frozen()
class ClientCredentials:
    id: UUID
    secret: str

    @classmethod
    def from_data(cls, data: ClientCredentialsData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> ClientCredentialsData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]
