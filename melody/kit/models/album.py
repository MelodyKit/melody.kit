from __future__ import annotations

from typing import List, Optional, Type, TypeVar, overload

from attrs import define, field
from edgedb import Object  # type: ignore
from iters import iter
from pendulum import Date, DateTime

from melody.kit.constants import DEFAULT_COUNT, DEFAULT_DURATION
from melody.kit.enums import AlbumType, EntityType
from melody.kit.models.entity import Entity, EntityData
from melody.kit.uri import URI
from melody.shared.converter import CONVERTER
from melody.shared.date_time import (
    convert_standard_date,
    convert_standard_date_time,
    utc_now,
    utc_today,
)

__all__ = (
    "Album",
    "AlbumData",
    "AlbumTracks",
    "AlbumTracksData",
    "album_from_object",
    "album_from_data",
    "album_into_data",
)


class AlbumData(EntityData):
    uri: str

    artists: List[ArtistData]

    album_type: str
    release_date: str

    duration_ms: int

    track_count: int

    label: Optional[str]

    genres: List[str]


A = TypeVar("A", bound="Album")


@define()
class Album(Entity):
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

    uri: URI = field()

    @uri.default
    def default_uri(self) -> URI:
        return URI(type=EntityType.ALBUM, id=self.id)

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
            label=object.label,
            genres=object.genres,
            created_at=convert_standard_date_time(object.created_at),
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
        )

    @classmethod
    def from_data(cls: Type[A], data: AlbumData) -> A:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> AlbumData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def album_from_object(object: Object) -> Album:
    ...


@overload
def album_from_object(object: Object, album_type: Type[A]) -> A:
    ...


def album_from_object(object: Object, album_type: Type[Album] = Album) -> Album:
    return album_type.from_object(object)


@overload
def album_from_data(data: AlbumData) -> Album:
    ...


@overload
def album_from_data(data: AlbumData, album_type: Type[A]) -> A:
    ...


def album_from_data(data: AlbumData, album_type: Type[Album] = Album) -> Album:
    return album_type.from_data(data)


def album_into_data(album: Album) -> AlbumData:
    return album.into_data()


from melody.kit.models.artist import Artist, ArtistData, artist_from_object
from melody.kit.models.track import PartialTrack, PartialTrackData


AlbumTracks = List[PartialTrack]
AlbumTracksData = List[PartialTrackData]
