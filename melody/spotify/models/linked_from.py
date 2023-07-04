from typing import Type, TypeVar

from attrs import define

from melody.shared.converter import CONVERTER, register_unstructure_hook_omit_client
from melody.spotify.models.entity import Entity, EntityData

__all__ = ("LinkedFrom", "LinkedFromData")


class LinkedFromData(EntityData):
    pass


L = TypeVar("L", bound="LinkedFrom")


@register_unstructure_hook_omit_client
@define()
class LinkedFrom(Entity):
    @classmethod
    def from_data(cls: Type[L], data: LinkedFromData) -> L:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> LinkedFromData:
        return CONVERTER.unstructure(self)  # type: ignore
