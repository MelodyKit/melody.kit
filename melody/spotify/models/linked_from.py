from attrs import define
from typing_extensions import Self

from melody.shared.converter import CONVERTER, register_unstructure_hook_omit_client
from melody.spotify.models.entity import Entity, EntityData

__all__ = ("LinkedFrom", "LinkedFromData")


class LinkedFromData(EntityData):
    pass


@register_unstructure_hook_omit_client
@define()
class LinkedFrom(Entity):
    @classmethod
    def from_data(cls, data: LinkedFromData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> LinkedFromData:
        return CONVERTER.unstructure(self)  # type: ignore
