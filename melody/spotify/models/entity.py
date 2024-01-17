from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from attrs import define, field
from typing_extensions import Self

from melody.shared.converter import CONVERTER, register_unstructure_hook_omit_client
from melody.spotify.enums import EntityType
from melody.spotify.models.base import Base, BaseData
from melody.spotify.uri import URI

if TYPE_CHECKING:
    from melody.spotify.client import Client

else:
    Client = Any

__all__ = ("Entity", "EntityData")

CLIENT_NOT_ATTACHED = "`client` not attached to the entity"


class EntityData(BaseData):
    id: str
    type: str
    uri: str
    href: str


@register_unstructure_hook_omit_client
@define()
class Entity(Base):
    id: str = field()
    type: EntityType = field()
    uri: URI = field()
    href: str = field()

    client_unchecked: Optional[Client] = field(default=None, repr=False, init=False, eq=False)

    @property
    def client(self) -> Client:
        client = self.client_unchecked

        if client is None:
            raise ValueError(CLIENT_NOT_ATTACHED)

        return client

    @client.setter
    def client(self, client: Client) -> None:
        self.client_unchecked = client

    @client.deleter
    def client(self) -> None:
        self.client_unchecked = None

    def attach_client(self, client: Client) -> Self:
        self.client = client

        return self

    def detach_client(self) -> Self:
        del self.client

        return self

    @classmethod
    def from_data(cls, data: EntityData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> EntityData:
        return CONVERTER.unstructure(self)  # type: ignore
