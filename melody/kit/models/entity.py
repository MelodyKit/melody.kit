from typing import Optional

from attrs import define
from edgedb import Object
from typing_extensions import Self

from melody.kit.models.named import Named, NamedData
from melody.shared.converter import CONVERTER

__all__ = ("Entity", "EntityData")


class EntityData(NamedData):
    spotify_id: Optional[str]
    apple_music_id: Optional[str]
    yandex_music_id: Optional[str]


@define(kw_only=True)
class Entity(Named):
    spotify_id: Optional[str] = None
    apple_music_id: Optional[str] = None
    yandex_music_id: Optional[str] = None

    @classmethod
    def from_object(cls, object: Object) -> Self:
        self = super().from_object(object)

        self.spotify_id = object.spotify_id
        self.apple_music_id = object.apple_music_id
        self.yandex_music_id = object.yandex_music_id

        return self

    @classmethod
    def from_data(cls, data: EntityData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> EntityData:
        return CONVERTER.unstructure(self)  # type: ignore
