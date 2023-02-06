from __future__ import annotations

from typing import List, Optional, Type, TypeVar

from attrs import define, field
from edgedb import Object  # type: ignore
from iters import iter
from pendulum import DateTime

from melody.kit.constants import DEFAULT_COUNT, DEFAULT_DURATION, DEFAULT_EXPLICIT
from melody.kit.enums import URIType
from melody.kit.models.base import Base, BaseData
from melody.kit.models.uri import URIData
from melody.kit.uri import URI
from melody.kit.utils import convert_standard_date_time, utc_now

__all__ = ("Track", "TrackData", "track_from_object", "track_into_data")


class TrackData(URIData, BaseData):
    album: AlbumData
    artists: List[ArtistData]

    explicit: bool

    duration_ms: int

    stream_count: int
    stream_duration_ms: int

    genres: List[str]


T = TypeVar("T", bound="Track")


@define()
class Track(Base):
    album: Album = field()
    artists: List[Artist] = field()

    explicit: bool = field(default=DEFAULT_EXPLICIT)

    duration_ms: int = field(default=DEFAULT_DURATION)

    stream_count: int = field(default=DEFAULT_COUNT)
    stream_duration_ms: int = field(default=DEFAULT_DURATION)

    genres: List[str] = field(factory=list)

    created_at: DateTime = field(factory=utc_now)

    spotify_id: Optional[str] = field(default=None)
    apple_music_id: Optional[str] = field(default=None)
    yandex_music_id: Optional[str] = field(default=None)

    @classmethod
    def from_object(cls: Type[T], object: Object) -> T:  # type: ignore
        return cls(
            id=object.id,
            name=object.name,
            album=album_from_object(object.album),
            artists=iter(object.artists).map(artist_from_object).list(),
            explicit=object.explicit,
            duration_ms=object.duration_ms,
            stream_count=object.stream_count,
            stream_duration_ms=object.stream_duration_ms,
            genres=object.genres,
            created_at=convert_standard_date_time(object.created_at),
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
        )

    def into_data(self) -> TrackData:
        return TrackData(
            id=str(self.id),
            name=self.name,
            created_at=str(self.created_at),
            spotify_id=self.spotify_id,
            apple_music_id=self.apple_music_id,
            yandex_music_id=self.yandex_music_id,
            uri=str(self.uri),
            album=album_into_data(self.album),
            artists=iter(self.artists).map(artist_into_data).list(),
            explicit=self.explicit,
            duration_ms=self.duration_ms,
            stream_count=self.stream_count,
            stream_duration_ms=self.stream_duration_ms,
            genres=self.genres,
        )

    @property
    def uri(self) -> URI:
        return URI(type=URIType.TRACK, id=self.id)


def track_from_object(object: Object) -> Track:
    return Track.from_object(object)


def track_into_data(track: Track) -> TrackData:
    return track.into_data()


from melody.kit.models.album import Album, AlbumData, album_from_object, album_into_data
from melody.kit.models.artist import Artist, ArtistData, artist_from_object, artist_into_data
