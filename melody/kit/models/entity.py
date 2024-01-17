from typing import Optional

from attrs import define, field
from edgedb import Object
from pendulum import DateTime
from typing_extensions import Self

from melody.kit.models.created_at import CreatedAt, CreatedAtData
from melody.shared.converter import CONVERTER
from melody.shared.date_time import convert_standard_date_time, utc_now

__all__ = ("Entity", "EntityData")


class EntityData(CreatedAtData):
    name: str

    spotify_id: Optional[str]
    apple_music_id: Optional[str]
    yandex_music_id: Optional[str]


@define()
class Entity(CreatedAt):
    name: str

    created_at: DateTime = field(factory=utc_now)

    spotify_id: Optional[str] = field(default=None)
    apple_music_id: Optional[str] = field(default=None)
    yandex_music_id: Optional[str] = field(default=None)

    @classmethod
    def from_object(cls, object: Object) -> Self:
        return cls(
            id=object.id,
            name=object.name,
            created_at=convert_standard_date_time(object.created_at),
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
        )

    @classmethod
    def from_data(cls, data: EntityData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> EntityData:
        return CONVERTER.unstructure(self)  # type: ignore
