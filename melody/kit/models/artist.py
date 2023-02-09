from typing import List, Optional, Type, TypeVar, overload

from attrs import define, field
from edgedb import Object  # type: ignore
from pendulum import DateTime

from melody.kit.constants import DEFAULT_COUNT, DEFAULT_DURATION
from melody.kit.enums import EntityType
from melody.kit.models.entity import Entity, EntityData
from melody.kit.uri import URI
from melody.shared.converter import CONVERTER
from melody.shared.date_time import convert_standard_date_time, utc_now

__all__ = (
    "Artist",
    "ArtistData",
    "ArtistTracks",
    "ArtistTracksData",
    "ArtistAlbums",
    "ArtistAlbumsData",
    "artist_from_object",
    "artist_from_data",
    "artist_into_data",
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
def artist_from_object(object: Object) -> Artist:
    ...


@overload
def artist_from_object(object: Object, artist_type: Type[A]) -> A:
    ...


def artist_from_object(object: Object, artist_type: Type[Artist] = Artist) -> Artist:
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

ArtistTracks = List[Track]
ArtistTracksData = List[TrackData]

ArtistAlbums = List[Album]
ArtistAlbumsData = List[AlbumData]
