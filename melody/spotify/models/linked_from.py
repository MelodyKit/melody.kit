from typing import Type, TypeVar

from attrs import define
from cattrs.gen import make_dict_unstructure_fn, override

from melody.shared.converter import CONVERTER
from melody.spotify.models.entity import Entity, EntityData

__all__ = ("LinkedFrom", "LinkedFromData")


class LinkedFromData(EntityData):
    pass


L = TypeVar("L", bound="LinkedFrom")


@define()
class LinkedFrom(Entity):
    @classmethod
    def from_data(cls: Type[L], data: LinkedFromData) -> L:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> LinkedFromData:
        return CONVERTER.unstructure(self)  # type: ignore


CONVERTER.register_unstructure_hook(
    LinkedFrom,
    make_dict_unstructure_fn(LinkedFrom, CONVERTER, client_unchecked=override(omit=True)),
)
