from __future__ import annotations

from typing import ClassVar, List, Optional

from attrs import define, field
from edgedb import Object
from iters.iters import iter
from typing_extensions import Self
from yarl import URL

from melody.kit.config import CONFIG
from melody.kit.constants import (
    DEFAULT_COUNT,
    DEFAULT_DURATION,
    DEFAULT_EXPLICIT,
    DEFAULT_POSITION,
)
from melody.kit.enums import EntityType
from melody.kit.links import (
    Linked,
    apple_music_track,
    self_track,
    spotify_track,
    yandex_music_track,
)
from melody.kit.models.entity import Entity, EntityData
from melody.kit.uri import Locatable
from melody.shared.converter import CONVERTER

__all__ = (
    # tracks
    "Track",
    "TrackData",
    # tracks with position
    "PositionTrack",
    "PositionTrackData",
)


class TrackData(EntityData):
    album: Optional[AlbumData]

    artists: List[ArtistData]

    explicit: bool

    duration_ms: int

    stream_count: int
    stream_duration_ms: int

    genres: List[str]


ALBUM_NOT_ATTACHED = "`album` is not attached"


@define(kw_only=True)
class Track(Linked, Locatable, Entity):
    TYPE: ClassVar[EntityType] = EntityType.TRACK

    album: Optional[Album] = field(default=None)

    artists: List[Artist] = field(factory=list)

    explicit: bool = field(default=DEFAULT_EXPLICIT)

    duration_ms: int = field(default=DEFAULT_DURATION)

    stream_count: int = field(default=DEFAULT_COUNT)
    stream_duration_ms: int = field(default=DEFAULT_DURATION)

    genres: List[str] = field(factory=list)

    def attach_album(self, album: Album) -> Self:
        self.album = album

        return self

    def detach_album(self) -> Self:
        self.album = None

        return self

    @property
    def required_album(self) -> Album:
        album = self.album

        if album is None:
            raise ValueError(ALBUM_NOT_ATTACHED)

        return album

    @classmethod
    def from_object(cls, object: Object) -> Self:
        self = super().from_object(object)

        try:
            album_object = object.album

        except AttributeError:
            album = None

        else:
            album = Album.from_object(album_object)

        self.album = album

        self.artists = iter(object.artists).map(Artist.from_object).list()

        self.explicit = object.explicit

        self.duration_ms = object.duration_ms

        self.stream_count = object.stream_count
        self.stream_duration_ms = object.stream_duration_ms

        self.genres = object.genres

        return self

    @classmethod
    def from_data(cls, data: TrackData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> TrackData:
        return CONVERTER.unstructure(self)  # type: ignore

    @property
    def spotify_url(self) -> Optional[URL]:
        spotify_id = self.spotify_id

        return None if spotify_id is None else URL(spotify_track(id=spotify_id))

    @property
    def apple_music_url(self) -> Optional[URL]:
        album = self.album

        if album is None:
            return None

        apple_music_id = self.apple_music_id
        apple_music_album_id = album.apple_music_id

        return (
            None
            if apple_music_id is None or apple_music_album_id is None
            else URL(apple_music_track(album_id=apple_music_album_id, id=apple_music_id))
        )

    @property
    def yandex_music_url(self) -> Optional[URL]:
        album = self.album

        if album is None:
            return None

        yandex_music_id = self.yandex_music_id
        yandex_music_album_id = album.yandex_music_id

        return (
            None
            if yandex_music_id is None or yandex_music_album_id is None
            else URL(yandex_music_track(album_id=yandex_music_album_id, id=yandex_music_id))
        )

    @property
    def url(self) -> URL:
        return URL(self_track(config=CONFIG, id=self.id))


class PositionTrackData(TrackData):
    position: int


AT_POSITION = "@position"


@define()
class PositionTrack(Track):
    position: int = DEFAULT_POSITION

    @classmethod
    def from_object(cls, object: Object) -> Self:
        self = super().from_object(object)

        self.position = object[AT_POSITION]

        return self

    @classmethod
    def from_data(cls, data: PositionTrackData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> PositionTrackData:
        return CONVERTER.unstructure(self)  # type: ignore


from melody.kit.models.album import Album, AlbumData
from melody.kit.models.artist import Artist, ArtistData
