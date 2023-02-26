from __future__ import annotations

from typing import List, Optional, Type, TypeVar, overload

from attrs import define, field
from edgedb import Object  # type: ignore
from iters import iter
from pendulum import DateTime

from melody.kit.constants import DEFAULT_COUNT, DEFAULT_DURATION, DEFAULT_EXPLICIT, DEFAULT_POSITION
from melody.kit.enums import EntityType
from melody.kit.models.entity import Entity, EntityData
from melody.kit.uri import URI
from melody.shared.converter import CONVERTER
from melody.shared.date_time import convert_standard_date_time, utc_now

__all__ = (
    "PartialTrack",
    "PartialTrackData",
    "partial_track_from_object",
    "partial_track_from_data",
    "partial_track_into_data",
    "Track",
    "TrackData",
    "track_from_object",
    "track_from_data",
    "track_into_data",
    "PositionTrack",
    "PositionTrackData",
    "position_track_from_object",
    "position_track_from_data",
    "position_track_into_data",
)


class PartialTrackData(EntityData):
    uri: str

    artists: List[ArtistData]

    explicit: bool

    duration_ms: int

    stream_count: int
    stream_duration_ms: int

    genres: List[str]


class TrackData(PartialTrackData):
    album: AlbumData


P = TypeVar("P", bound="PartialTrack")


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
    def from_object(cls: Type[P], object: Object) -> P:  # type: ignore
        return cls(
            id=object.id,
            name=object.name,
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

    @classmethod
    def from_data(cls: Type[P], data: PartialTrackData) -> P:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> PartialTrackData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def partial_track_from_object(object: Object) -> PartialTrack:
    ...


@overload
def partial_track_from_object(object: Object, partial_track_type: Type[P]) -> P:
    ...


def partial_track_from_object(
    object: Object, partial_track_type: Type[PartialTrack] = PartialTrack
) -> PartialTrack:
    return partial_track_type.from_object(object)


@overload
def partial_track_from_data(data: PartialTrackData) -> PartialTrack:
    ...


@overload
def partial_track_from_data(data: PartialTrackData, partial_track_type: Type[P]) -> P:
    ...


def partial_track_from_data(
    data: PartialTrackData, partial_track_type: Type[PartialTrack] = PartialTrack
) -> PartialTrack:
    return partial_track_type.from_data(data)


def partial_track_into_data(partial_track: PartialTrack) -> PartialTrackData:
    return partial_track.into_data()


T = TypeVar("T", bound="Track")


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

    @classmethod
    def from_data(cls: Type[T], data: TrackData) -> T:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> TrackData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def track_from_object(object: Object) -> Track:
    ...


@overload
def track_from_object(object: Object, track_type: Type[T]) -> T:
    ...


def track_from_object(object: Object, track_type: Type[Track] = Track) -> Track:
    return track_type.from_object(object)


@overload
def track_from_data(data: TrackData) -> Track:
    ...


@overload
def track_from_data(data: TrackData, track_type: Type[T]) -> T:
    ...


def track_from_data(data: TrackData, track_type: Type[Track] = Track) -> Track:
    return track_type.from_data(data)


def track_into_data(track: Track) -> TrackData:
    return track.into_data()


class PositionTrackData(TrackData):
    position: int


AT_POSITION = "@position"

PT = TypeVar("PT", bound="PositionTrack")


@define()
class PositionTrack(Track):
    position: int = DEFAULT_POSITION

    @classmethod
    def from_object(cls: Type[PT], object: Object) -> PT:  # type: ignore
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
            position=object[AT_POSITION],
            created_at=convert_standard_date_time(object.created_at),
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
        )

    @classmethod
    def from_data(cls: Type[PT], data: PositionTrackData) -> PT:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> PositionTrackData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def position_track_from_object(object: Object) -> PositionTrack:
    ...


@overload
def position_track_from_object(object: Object, position_track_type: Type[PT]) -> PT:
    ...


def position_track_from_object(
    object: Object, position_track_type: Type[PositionTrack] = PositionTrack
) -> PositionTrack:
    return position_track_type.from_object(object)


@overload
def position_track_from_data(data: PositionTrackData) -> PositionTrack:
    ...


@overload
def position_track_from_data(data: PositionTrackData, position_track_type: Type[PT]) -> PT:
    ...


def position_track_from_data(
    data: PositionTrackData, position_track_type: Type[PositionTrack] = PositionTrack
) -> PositionTrack:
    return position_track_type.from_data(data)


def position_track_into_data(position_track: PositionTrack) -> PositionTrackData:
    return position_track.into_data()


from melody.kit.models.album import Album, AlbumData, album_from_object
from melody.kit.models.artist import Artist, ArtistData, artist_from_object
