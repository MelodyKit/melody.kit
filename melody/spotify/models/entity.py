from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Type, TypeVar

from attrs import define
from cattrs.gen import make_dict_unstructure_fn, override

from melody.shared.converter import CONVERTER
from melody.spotify.enums import EntityType
from melody.spotify.models.base import Base, BaseData
from melody.spotify.uri import URI

if TYPE_CHECKING:
    from melody.spotify.client import Client

__all__ = ("Entity", "EntityData")

CLIENT_NOT_ATTACHED = "`client` not attached to the entity"

E = TypeVar("E", bound="Entity")


class EntityData(BaseData):
    id: str
    type: str
    uri: str
    name: str
    href: str


@define()
class Entity(Base):
    id: str
    type: EntityType
    uri: URI
    name: str
    href: str

    client_unchecked: Optional[Client] = None

    @property
    def client(self) -> Client:
        client = self.client_unchecked

        if client is None:
            raise RuntimeError(CLIENT_NOT_ATTACHED)

        return client

    @client.setter
    def client(self, client: Client) -> None:
        self.client_unchecked = client

    @client.deleter
    def client(self) -> None:
        self.client_unchecked = None

    def attach_client(self: E, client: Client) -> E:
        self.client = client

        return self

    def detach_client(self: E) -> E:
        del self.client

        return self

    @classmethod
    def from_data(cls: Type[E], data: EntityData) -> E:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> EntityData:
        return CONVERTER.unstructure(self)  # type: ignore


if not TYPE_CHECKING:
    Client = Any


CONVERTER.register_unstructure_hook(
    Entity,
    make_dict_unstructure_fn(Entity, CONVERTER, client_unchecked=override(omit=True)),
)