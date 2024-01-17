from __future__ import annotations

from typing import List, Optional

from attrs import define, field
from edgedb import Object
from iters.iters import iter
from pendulum import DateTime
from typing_extensions import Self

from melody.kit.constants import (
    DEFAULT_COUNT,
    DEFAULT_DURATION,
    DEFAULT_EXPLICIT,
    DEFAULT_POSITION,
)
from melody.kit.enums import EntityType
from melody.kit.models.entity import Entity, EntityData
from melody.kit.uri import URI
from melody.shared.converter import CONVERTER
from melody.shared.date_time import convert_standard_date_time, utc_now

__all__ = (
    # partial tracks
    "PartialTrack",
    "PartialTrackData",
    # tracks
    "Track",
    "TrackData",
    # tracks with position
    "PositionTrack",
    "PositionTrackData",
)


class PartialTrackData(EntityData):
    uri: str

    artists: List[ArtistData]

    explicit: bool

    duration_ms: int

    stream_count: int
    stream_duration_ms: int

    genres: List[str]


@define()
class PartialTrack(Entity):
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

    uri: URI = field()

    @uri.default
    def default_uri(self) -> URI:
        return URI(type=EntityType.TRACK, id=self.id)

    @classmethod
    def from_object(cls, object: Object) -> Self:
        return cls(
            id=object.id,
            name=object.name,
            artists=iter(object.artists).map(Artist.from_object).list(),
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

    @classmethod
    def from_data(cls, data: PartialTrackData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> PartialTrackData:
        return CONVERTER.unstructure(self)  # type: ignore


class TrackData(PartialTrackData):
    album: AlbumData


@define()
class Track(PartialTrack):
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

    uri: URI = field()

    @uri.default
    def default_uri(self) -> URI:
        return URI(type=EntityType.TRACK, id=self.id)

    @classmethod
    def from_object(cls, object: Object) -> Self:
        return cls(
            id=object.id,
            name=object.name,
            album=Album.from_object(object.album),
            artists=iter(object.artists).map(Artist.from_object).list(),
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

    @classmethod
    def from_data(cls, data: TrackData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> TrackData:
        return CONVERTER.unstructure(self)  # type: ignore


class PositionTrackData(TrackData):
    position: int


AT_POSITION = "@position"


@define()
class PositionTrack(Track):
    position: int = DEFAULT_POSITION

    @classmethod
    def from_object(cls, object: Object) -> Self:
        return cls(
            id=object.id,
            name=object.name,
            album=Album.from_object(object.album),
            artists=iter(object.artists).map(Artist.from_object).list(),
            explicit=object.explicit,
            duration_ms=object.duration_ms,
            stream_count=object.stream_count,
            stream_duration_ms=object.stream_duration_ms,
            genres=object.genres,
            position=object[AT_POSITION],  # NOTE: can not be accessed through an attribute
            created_at=convert_standard_date_time(object.created_at),
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
        )

    @classmethod
    def from_data(cls, data: PositionTrackData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> PositionTrackData:
        return CONVERTER.unstructure(self)  # type: ignore


from melody.kit.models.album import Album, AlbumData
from melody.kit.models.artist import Artist, ArtistData
