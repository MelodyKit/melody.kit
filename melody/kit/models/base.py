from typing import Optional, Type, TypeVar

from attrs import define, field
from edgedb import Object  # type: ignore
from pendulum import DateTime

from melody.kit.models.abstract import Abstract, AbstractData
from melody.kit.utils import convert_standard_date_time, utc_now

__all__ = ("Base", "BaseData", "base_from_object", "base_into_data")


class BaseData(AbstractData):
    name: str

    created_at: str

    spotify_id: Optional[str]
    apple_music_id: Optional[str]
    yandex_music_id: Optional[str]


B = TypeVar("B", bound="Base")


@define()
class Base(Abstract):
    name: str

    created_at: DateTime = field(factory=utc_now)

    spotify_id: Optional[str] = field(default=None)
    apple_music_id: Optional[str] = field(default=None)
    yandex_music_id: Optional[str] = field(default=None)

    @classmethod
    def from_object(cls: Type[B], object: Object) -> B:  # type: ignore
        return cls(
            id=object.id,
            name=object.name,
            created_at=convert_standard_date_time(object.created_at),
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
        )

    def into_data(self) -> BaseData:
        return BaseData(
            id=str(self.id),
            name=self.name,
            created_at=str(self.created_at),
            spotify_id=self.spotify_id,
            apple_music_id=self.apple_music_id,
            yandex_music_id=self.yandex_music_id,
        )


def base_from_object(object: Object) -> Base:
    return Base.from_object(object)


def base_into_data(base: Base) -> BaseData:
    return base.into_data()
