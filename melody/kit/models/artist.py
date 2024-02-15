from typing import ClassVar, List, Optional

from attrs import define, field
from edgedb import Object
from typing_extensions import Self
from yarl import URL

from melody.kit.config import CONFIG
from melody.kit.constants import DEFAULT_COUNT, DEFAULT_DURATION
from melody.kit.enums import EntityType
from melody.kit.links import (
    Linked,
    apple_music_artist,
    self_artist,
    spotify_artist,
    yandex_music_artist,
)
from melody.kit.models.entity import Entity, EntityData
from melody.kit.models.pagination import Pagination, PaginationData
from melody.kit.uri import Locatable
from melody.shared.converter import CONVERTER
from melody.shared.typing import Data

__all__ = (
    # artists
    "Artist",
    "ArtistData",
    # artist tracks
    "ArtistTracks",
    "ArtistTracksData",
    # artist albums
    "ArtistAlbums",
    "ArtistAlbumsData",
)


class ArtistData(EntityData):
    follower_count: int

    stream_count: int
    stream_duration_ms: int

    genres: List[str]


@define(kw_only=True)
class Artist(Linked, Locatable, Entity):
    TYPE: ClassVar[EntityType] = EntityType.ARTIST

    follower_count: int = field(default=DEFAULT_COUNT)

    stream_count: int = field(default=DEFAULT_COUNT)
    stream_duration_ms: int = field(default=DEFAULT_DURATION)

    genres: List[str] = field(factory=list)

    @classmethod
    def from_object(cls, object: Object) -> Self:
        self = super().from_object(object)

        self.follower_count = object.follower_count

        self.stream_count = object.stream_count
        self.stream_duration_ms = object.stream_duration_ms

        self.genres = object.genres

        return self

    @classmethod
    def from_data(cls, data: ArtistData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> ArtistData:
        return CONVERTER.unstructure(self)  # type: ignore

    @property
    def spotify_url(self) -> Optional[URL]:
        spotify_id = self.spotify_id

        return None if spotify_id is None else URL(spotify_artist(id=spotify_id))

    @property
    def apple_music_url(self) -> Optional[URL]:
        apple_music_id = self.apple_music_id

        return None if apple_music_id is None else URL(apple_music_artist(id=apple_music_id))

    @property
    def yandex_music_url(self) -> Optional[URL]:
        yandex_music_id = self.yandex_music_id

        return None if yandex_music_id is None else URL(yandex_music_artist(id=yandex_music_id))

    @property
    def url(self) -> URL:
        return URL(self_artist(config=CONFIG, id=self.id))


from melody.kit.models.album import Album, AlbumData
from melody.kit.models.tracks import Track, TrackData


class ArtistTracksData(Data):
    items: List[TrackData]
    pagination: PaginationData


@define()
class ArtistTracks:
    items: List[Track] = field(factory=list)
    pagination: Pagination = field(factory=Pagination)

    @classmethod
    def from_data(cls, data: ArtistTracksData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> ArtistTracksData:
        return CONVERTER.unstructure(self)  # type: ignore


class ArtistAlbumsData(Data):
    items: List[AlbumData]
    pagination: PaginationData


@define()
class ArtistAlbums:
    items: List[Album] = field(factory=list)
    pagination: Pagination = field(factory=Pagination)

    @classmethod
    def from_data(cls, data: ArtistAlbumsData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> ArtistAlbumsData:
        return CONVERTER.unstructure(self)  # type: ignore
