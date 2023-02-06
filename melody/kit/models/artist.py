from typing import List, Optional, Type, TypeVar

from attrs import define, field
from edgedb import Object  # type: ignore
from pendulum import DateTime

from melody.kit.constants import DEFAULT_COUNT, DEFAULT_DURATION
from melody.kit.enums import URIType
from melody.kit.models.base import Base, BaseData
from melody.kit.models.uri import URIData
from melody.kit.uri import URI
from melody.kit.utils import convert_standard_date_time, utc_now

__all__ = (
    "Artist",
    "ArtistData",
    "ArtistTracks",
    "ArtistTracksData",
    "ArtistAlbums",
    "ArtistAlbumsData",
    "artist_from_object",
    "artist_into_data",
)


class ArtistData(URIData, BaseData):
    follower_count: int

    stream_count: int
    stream_duration_ms: int

    genres: List[str]


A = TypeVar("A", bound="Artist")


@define()
class Artist(Base):
    follower_count: int = field(default=DEFAULT_COUNT)

    stream_count: int = field(default=DEFAULT_COUNT)
    stream_duration_ms: int = field(default=DEFAULT_DURATION)

    genres: List[str] = field(factory=list)

    created_at: DateTime = field(factory=utc_now)

    spotify_id: Optional[str] = field(default=None)
    apple_music_id: Optional[str] = field(default=None)
    yandex_music_id: Optional[str] = field(default=None)

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

    def into_data(self) -> ArtistData:
        return ArtistData(
            id=str(self.id),
            name=self.name,
            created_at=str(self.created_at),
            spotify_id=self.spotify_id,
            apple_music_id=self.apple_music_id,
            yandex_music_id=self.yandex_music_id,
            uri=str(self.uri),
            follower_count=self.follower_count,
            stream_count=self.stream_count,
            stream_duration_ms=self.stream_duration_ms,
            genres=self.genres,
        )

    @property
    def uri(self) -> URI:
        return URI(type=URIType.ARTIST, id=self.id)


def artist_from_object(object: Object) -> Artist:
    return Artist.from_object(object)


def artist_into_data(artist: Artist) -> ArtistData:
    return artist.into_data()


from melody.kit.models.album import Album, AlbumData
from melody.kit.models.track import Track, TrackData

ArtistTracks = List[Track]
ArtistTracksData = List[TrackData]

ArtistAlbums = List[Album]
ArtistAlbumsData = List[AlbumData]
