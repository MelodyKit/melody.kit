from typing import List, Optional

from attrs import define, field
from edgedb import Object
from pendulum import DateTime
from typing_extensions import Self

from melody.kit.constants import DEFAULT_COUNT, DEFAULT_DURATION
from melody.kit.enums import EntityType
from melody.kit.models.entity import Entity, EntityData
from melody.kit.models.pagination import Pagination, PaginationData
from melody.kit.uri import URI
from melody.shared.converter import CONVERTER
from melody.shared.date_time import convert_standard_date_time, utc_now
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
    uri: str

    follower_count: int

    stream_count: int
    stream_duration_ms: int

    genres: List[str]


@define()
class Artist(Entity):
    follower_count: int = field(default=DEFAULT_COUNT)

    stream_count: int = field(default=DEFAULT_COUNT)
    stream_duration_ms: int = field(default=DEFAULT_DURATION)

    genres: List[str] = field(factory=list)

    created_at: DateTime = field(factory=utc_now)

    spotify_id: Optional[str] = field(default=None)
    apple_music_id: Optional[str] = field(default=None)
    yandex_music_id: Optional[str] = field(default=None)

    uri: URI = field()

    @uri.default
    def default_uri(self) -> URI:
        return URI(type=EntityType.ARTIST, id=self.id)

    @classmethod
    def from_object(cls, object: Object) -> Self:
        return cls(
            id=object.id,
            name=object.name,
            follower_count=object.follower_count,
            stream_count=object.stream_count,
            stream_duration_ms=object.stream_duration_ms,
            genres=object.genres,
            created_at=convert_standard_date_time(object.created_at),
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
        )

    @classmethod
    def from_data(cls, data: ArtistData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> ArtistData:
        return CONVERTER.unstructure(self)  # type: ignore


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
