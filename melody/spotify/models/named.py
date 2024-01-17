from attrs import define
from typing_extensions import Self

from melody.shared.converter import CONVERTER, register_unstructure_hook_omit_client
from melody.spotify.models.entity import Entity, EntityData

__all__ = ("Named", "NamedData")


class NamedData(EntityData):
    name: str


@register_unstructure_hook_omit_client
@define()
class Named(Entity):
    name: str

    @classmethod
    def from_data(cls, data: NamedData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> NamedData:
        return CONVERTER.unstructure(self)  # type: ignore
