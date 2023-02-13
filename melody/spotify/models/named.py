from typing import Type, TypeVar

from attrs import define
from cattrs.gen import make_dict_unstructure_fn, override

from melody.shared.converter import CONVERTER
from melody.spotify.models.entity import Entity, EntityData

__all__ = ("Named", "NamedData")


class NamedData(EntityData):
    name: str


N = TypeVar("N", bound="Named")


@define()
class Named(Entity):
    name: str

    @classmethod
    def from_data(cls: Type[N], data: NamedData) -> N:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> NamedData:
        return CONVERTER.unstructure(self)  # type: ignore


CONVERTER.register_unstructure_hook(
    Named,
    make_dict_unstructure_fn(Named, CONVERTER, client_unchecked=override(omit=True)),
)
