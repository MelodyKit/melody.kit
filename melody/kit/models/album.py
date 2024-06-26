from __future__ import annotations

from typing import ClassVar, List, Optional

from attrs import Factory, define
from edgedb import Object
from iters.iters import iter
from pendulum import Date
from typing_extensions import Self
from yarl import URL

from melody.kit.config.core import CONFIG
from melody.kit.constants import DEFAULT_COUNT, DEFAULT_DURATION
from melody.kit.enums import AlbumType, EntityType
from melody.kit.links import (
    Linked,
    apple_music_album,
    self_album,
    spotify_album,
    yandex_music_album,
)
from melody.kit.models.entity import Entity, EntityData
from melody.kit.models.pagination import Pagination, PaginationData
from melody.kit.uri import Locatable
from melody.shared.converter import CONVERTER
from melody.shared.time import convert_standard_date, utc_today
from melody.shared.typing import Data

__all__ = (
    # albums
    "Album",
    "AlbumData",
    # album tracks
    "AlbumTracks",
    "AlbumTracksData",
)


class AlbumData(EntityData):
    artists: List[ArtistData]

    album_type: str
    release_date: str

    duration_ms: int

    track_count: int

    label: Optional[str]

    genres: List[str]


@define(kw_only=True)
class Album(Linked, Locatable, Entity):
    TYPE: ClassVar[EntityType] = EntityType.ALBUM

    artists: List[Artist] = Factory(list)

    album_type: AlbumType = AlbumType.DEFAULT
    release_date: Date = Factory(utc_today)

    duration_ms: int = DEFAULT_DURATION

    track_count: int = DEFAULT_COUNT

    label: Optional[str] = None

    genres: List[str] = Factory(list)

    @classmethod
    def from_object(cls, object: Object) -> Self:
        self = super().from_object(object)

        self.artists = iter(object.artists).map(Artist.from_object).list()

        self.album_type = AlbumType(object.album_type.value)
        self.release_date = convert_standard_date(object.release_date)

        self.duration_ms = object.duration_ms

        self.track_count = object.track_count

        self.label = object.label

        self.genres = object.genres

        return self

    @classmethod
    def from_data(cls, data: AlbumData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> AlbumData:
        return CONVERTER.unstructure(self)  # type: ignore

    @property
    def spotify_url(self) -> Optional[URL]:
        spotify_id = self.spotify_id

        return None if spotify_id is None else URL(spotify_album(id=spotify_id))

    @property
    def apple_music_url(self) -> Optional[URL]:
        apple_music_id = self.apple_music_id

        return None if apple_music_id is None else URL(apple_music_album(id=apple_music_id))

    @property
    def yandex_music_url(self) -> Optional[URL]:
        yandex_music_id = self.yandex_music_id

        return None if yandex_music_id is None else URL(yandex_music_album(id=yandex_music_id))

    @property
    def url(self) -> URL:
        return URL(self_album(config=CONFIG, id=self.id))


from melody.kit.models.artist import Artist, ArtistData
from melody.kit.models.tracks import Track, TrackData


class AlbumTracksData(Data):
    items: List[TrackData]
    pagination: PaginationData


@define()
class AlbumTracks:
    items: List[Track] = Factory(list)
    pagination: Pagination = Factory(Pagination)

    @classmethod
    def from_data(cls, data: AlbumTracksData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> AlbumTracksData:
        return CONVERTER.unstructure(self)  # type: ignore
