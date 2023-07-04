from typing import Type, TypeVar

from attrs import define

from melody.shared.converter import CONVERTER, register_unstructure_hook_omit_client
from melody.spotify.models.entity import Entity, EntityData

__all__ = ("Named", "NamedData")


class NamedData(EntityData):
    name: str


N = TypeVar("N", bound="Named")


@register_unstructure_hook_omit_client
@define()
class Named(Entity):
    name: str

    @classmethod
    def from_data(cls: Type[N], data: NamedData) -> N:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> NamedData:
        return CONVERTER.unstructure(self)  # type: ignore
