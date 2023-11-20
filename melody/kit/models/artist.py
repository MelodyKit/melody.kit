from typing import List, Optional, Type
from typing import TypedDict as Data
from typing import TypeVar, overload

from attrs import define, field
from edgedb import Object  # type: ignore
from pendulum import DateTime

from melody.kit.constants import DEFAULT_COUNT, DEFAULT_DURATION
from melody.kit.enums import EntityType
from melody.kit.models.entity import Entity, EntityData
from melody.kit.models.pagination import Pagination, PaginationData
from melody.kit.uri import URI
from melody.shared.converter import CONVERTER
from melody.shared.date_time import convert_standard_date_time, utc_now

__all__ = (
    # artists
    "Artist",
    "ArtistData",
    "artist_from_object",
    "artist_from_data",
    "artist_into_data",
    # artist tracks
    "ArtistTracks",
    "ArtistTracksData",
    "artist_tracks_from_data",
    "artist_tracks_into_data",
    # artist albums
    "ArtistAlbums",
    "ArtistAlbumsData",
    "artist_albums_from_data",
    "artist_albums_into_data",
)


class ArtistData(EntityData):
    uri: str

    follower_count: int

    stream_count: int
    stream_duration_ms: int

    genres: List[str]


A = TypeVar("A", bound="Artist")


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
    def from_object(cls: Type[A], object: Object) -> A:  # type: ignore
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
    def from_data(cls: Type[A], data: ArtistData) -> A:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> ArtistData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def artist_from_object(object: Object) -> Artist:  # type: ignore
    ...


@overload
def artist_from_object(object: Object, artist_type: Type[A]) -> A:  # type: ignore
    ...


def artist_from_object(
    object: Object, artist_type: Type[Artist] = Artist  # type: ignore
) -> Artist:
    return artist_type.from_object(object)


@overload
def artist_from_data(data: ArtistData) -> Artist:
    ...


@overload
def artist_from_data(data: ArtistData, artist_type: Type[A]) -> A:
    ...


def artist_from_data(data: ArtistData, artist_type: Type[Artist] = Artist) -> Artist:
    return artist_type.from_data(data)


def artist_into_data(artist: Artist) -> ArtistData:
    return artist.into_data()


from melody.kit.models.album import Album, AlbumData
from melody.kit.models.track import Track, TrackData


class ArtistTracksData(Data):
    items: List[TrackData]
    pagination: PaginationData


AT = TypeVar("AT", bound="ArtistTracks")


@define()
class ArtistTracks:
    items: List[Track] = field(factory=list)
    pagination: Pagination = field(factory=Pagination)

    @classmethod
    def from_data(cls: Type[AT], data: ArtistTracksData) -> AT:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> ArtistTracksData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def artist_tracks_from_data(data: ArtistTracksData) -> ArtistTracks:
    ...


@overload
def artist_tracks_from_data(data: ArtistTracksData, artist_tracks_type: Type[AT]) -> AT:
    ...


def artist_tracks_from_data(
    data: ArtistTracksData, artist_tracks_type: Type[ArtistTracks] = ArtistTracks
) -> ArtistTracks:
    return artist_tracks_type.from_data(data)


def artist_tracks_into_data(artist_tracks: ArtistTracks) -> ArtistTracksData:
    return artist_tracks.into_data()


class ArtistAlbumsData(Data):
    items: List[AlbumData]
    pagination: PaginationData


AA = TypeVar("AA", bound="ArtistAlbums")


@define()
class ArtistAlbums:
    items: List[Album] = field(factory=list)
    pagination: Pagination = field(factory=Pagination)

    @classmethod
    def from_data(cls: Type[AA], data: ArtistAlbumsData) -> AA:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> ArtistAlbumsData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def artist_albums_from_data(data: ArtistAlbumsData) -> ArtistAlbums:
    ...


@overload
def artist_albums_from_data(data: ArtistAlbumsData, artist_albums_type: Type[AA]) -> AA:
    ...


def artist_albums_from_data(
    data: ArtistAlbumsData, artist_albums_type: Type[ArtistAlbums] = ArtistAlbums
) -> ArtistAlbums:
    return artist_albums_type.from_data(data)


def artist_albums_into_data(artist_albums: ArtistAlbums) -> ArtistAlbumsData:
    return artist_albums.into_data()
