from __future__ import annotations

from typing import List, Optional, Type, TypeVar

from attrs import define, field
from edgedb import Object  # type: ignore
from iters import iter
from pendulum import Date, DateTime

from melody.kit.constants import DEFAULT_COUNT, DEFAULT_DURATION
from melody.kit.enums import AlbumType, URIType
from melody.kit.models.base import Base, BaseData
from melody.kit.models.uri import URIData
from melody.kit.uri import URI
from melody.kit.utils import convert_standard_date, convert_standard_date_time, utc_now, utc_today

__all__ = (
    "Album",
    "AlbumData",
    "AlbumTracks",
    "AlbumTracksData",
    "album_from_object",
    "album_into_data",
)


class AlbumData(URIData, BaseData):
    artists: List[ArtistData]

    album_type: str
    release_date: str

    duration_ms: int

    track_count: int

    label: Optional[str]

    genres: List[str]


A = TypeVar("A", bound="Album")


@define()
class Album(Base):
    artists: List[Artist] = field()

    album_type: AlbumType = field(default=AlbumType.DEFAULT)
    release_date: Date = field(factory=utc_today)

    duration_ms: int = field(default=DEFAULT_DURATION)

    track_count: int = field(default=DEFAULT_COUNT)

    label: Optional[str] = field(default=None)

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
            artists=iter(object.artists).map(artist_from_object).list(),
            album_type=AlbumType(object.album_type.value),
            release_date=convert_standard_date(object.release_date),
            duration_ms=object.duration_ms,
            track_count=object.track_count,
            genres=object.genres,
            created_at=convert_standard_date_time(object.created_at),
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
        )

    def into_data(self) -> AlbumData:
        return AlbumData(
            id=str(self.id),
            name=self.name,
            created_at=str(self.created_at),
            spotify_id=self.spotify_id,
            apple_music_id=self.apple_music_id,
            yandex_music_id=self.yandex_music_id,
            uri=str(self.uri),
            artists=iter(self.artists).map(artist_into_data).list(),
            album_type=self.album_type.value,
            release_date=str(self.release_date),
            duration_ms=self.duration_ms,
            track_count=self.track_count,
            label=self.label,
            genres=self.genres,
        )

    @property
    def uri(self) -> URI:
        return URI(type=URIType.ALBUM, id=self.id)


def album_from_object(object: Object) -> Album:
    return Album.from_object(object)


def album_into_data(album: Album) -> AlbumData:
    return album.into_data()


from melody.kit.models.artist import Artist, ArtistData, artist_from_object, artist_into_data
from melody.kit.models.track import Track, TrackData

AlbumTracks = List[Track]
AlbumTracksData = List[TrackData]
