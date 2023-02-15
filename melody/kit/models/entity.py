from typing import Optional, Type, TypeVar, overload

from attrs import define, field
from edgedb import Object  # type: ignore
from pendulum import DateTime

from melody.kit.models.created_at import CreatedAt, CreatedAtData
from melody.shared.converter import CONVERTER
from melody.shared.date_time import convert_standard_date_time, utc_now

__all__ = ("Entity", "EntityData", "entity_from_object", "entity_from_data", "entity_into_data")


class EntityData(CreatedAtData):
    name: str

    spotify_id: Optional[str]
    apple_music_id: Optional[str]
    yandex_music_id: Optional[str]


E = TypeVar("E", bound="Entity")


@define()
class Entity(CreatedAt):
    name: str

    created_at: DateTime = field(factory=utc_now)

    spotify_id: Optional[str] = field(default=None)
    apple_music_id: Optional[str] = field(default=None)
    yandex_music_id: Optional[str] = field(default=None)

    @classmethod
    def from_object(cls: Type[E], object: Object) -> E:  # type: ignore
        return cls(
            id=object.id,
            name=object.name,
            created_at=convert_standard_date_time(object.created_at),
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
        )

    @classmethod
    def from_data(cls: Type[E], data: EntityData) -> E:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> EntityData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def entity_from_object(object: Object) -> Entity:
    ...


@overload
def entity_from_object(object: Object, entity_type: Type[E]) -> E:
    ...


def entity_from_object(object: Object, entity_type: Type[Entity] = Entity) -> Entity:
    return entity_type.from_object(object)


@overload
def entity_from_data(data: EntityData) -> Entity:
    ...


@overload
def entity_from_data(data: EntityData, entity_type: Type[E]) -> E:
    ...


def entity_from_data(data: EntityData, entity_type: Type[Entity] = Entity) -> Entity:
    return entity_type.from_data(data)


def entity_into_data(entity: Entity) -> EntityData:
    return entity.into_data()
