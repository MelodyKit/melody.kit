from __future__ import annotations

from typing import List, Optional, Type, TypeVar, overload

from attrs import define, field
from edgedb import Object  # type: ignore
from pendulum import DateTime

from melody.kit.constants import DEFAULT_COUNT, DEFAULT_DURATION
from melody.kit.enums import EntityType, PrivacyType
from melody.kit.models.entity import Entity, EntityData
from melody.kit.uri import URI
from melody.shared.constants import EMPTY
from melody.shared.converter import CONVERTER
from melody.shared.date_time import convert_standard_date_time, utc_now

__all__ = (
    "PartialPlaylist",
    "PartialPlaylistData",
    "partial_playlist_from_object",
    "partial_playlist_from_data",
    "partial_playlist_into_data",
    "Playlist",
    "PlaylistData",
    "PlaylistTracks",
    "PlaylistTracksData",
    "playlist_from_object",
    "playlist_from_data",
    "playlist_into_data",
)


class PartialPlaylistData(EntityData):
    uri: str

    description: str

    duration_ms: int

    track_count: int
    privacy_type: str


class PlaylistData(PartialPlaylistData):
    user: UserData


Q = TypeVar("Q", bound="PartialPlaylist")


@define()
class PartialPlaylist(Entity):
    description: str = field(default=EMPTY)

    duration_ms: int = field(default=DEFAULT_DURATION)

    track_count: int = field(default=DEFAULT_COUNT)

    privacy_type: PrivacyType = field(default=PrivacyType.DEFAULT)

    created_at: DateTime = field(factory=utc_now)

    spotify_id: Optional[str] = field(default=None)
    apple_music_id: Optional[str] = field(default=None)
    yandex_music_id: Optional[str] = field(default=None)

    uri: URI = field()

    @uri.default
    def default_uri(self) -> URI:
        return URI(type=EntityType.PLAYLIST, id=self.id)

    @classmethod
    def from_object(cls: Type[Q], object: Object) -> Q:  # type: ignore
        return cls(
            id=object.id,
            name=object.name,
            description=object.description,
            duration_ms=object.duration_ms,
            track_count=object.track_count,
            privacy_type=PrivacyType(object.privacy_type.value),
            created_at=convert_standard_date_time(object.created_at),
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
        )

    @classmethod
    def from_data(cls: Type[Q], data: PartialPlaylistData) -> Q:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> PartialPlaylistData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def partial_playlist_from_object(object: Object) -> PartialPlaylist:
    ...


@overload
def partial_playlist_from_object(object: Object, partial_playlist_type: Type[Q]) -> Q:
    ...


def partial_playlist_from_object(
    object: Object, partial_playlist_type: Type[PartialPlaylist] = PartialPlaylist
) -> PartialPlaylist:
    return partial_playlist_type.from_object(object)


@overload
def partial_playlist_from_data(data: PartialPlaylistData) -> PartialPlaylist:
    ...


@overload
def partial_playlist_from_data(data: PartialPlaylistData, playlist_type: Type[Q]) -> Q:
    ...


def partial_playlist_from_data(
    data: PartialPlaylistData, playlist_type: Type[PartialPlaylist] = PartialPlaylist
) -> PartialPlaylist:
    return playlist_type.from_data(data)


def partial_playlist_into_data(playlist: PartialPlaylist) -> PartialPlaylistData:
    return playlist.into_data()


P = TypeVar("P", bound="Playlist")


@define()
class Playlist(Entity):
    user: User = field()

    description: str = field(default=EMPTY)

    duration_ms: int = field(default=DEFAULT_DURATION)

    track_count: int = field(default=DEFAULT_COUNT)

    privacy_type: PrivacyType = field(default=PrivacyType.DEFAULT)

    created_at: DateTime = field(factory=utc_now)

    spotify_id: Optional[str] = field(default=None)
    apple_music_id: Optional[str] = field(default=None)
    yandex_music_id: Optional[str] = field(default=None)

    uri: URI = field()

    @uri.default
    def default_uri(self) -> URI:
        return URI(type=EntityType.PLAYLIST, id=self.id)

    @classmethod
    def from_object(cls: Type[P], object: Object) -> P:  # type: ignore
        return cls(
            id=object.id,
            name=object.name,
            user=user_from_object(object.user),
            description=object.description,
            duration_ms=object.duration_ms,
            track_count=object.track_count,
            privacy_type=PrivacyType(object.privacy_type.value),
            created_at=convert_standard_date_time(object.created_at),
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
        )

    @classmethod
    def from_data(cls: Type[P], data: PlaylistData) -> P:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> PlaylistData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def playlist_from_object(object: Object) -> Playlist:
    ...


@overload
def playlist_from_object(object: Object, playlist_type: Type[P]) -> P:
    ...


def playlist_from_object(object: Object, playlist_type: Type[Playlist] = Playlist) -> Playlist:
    return playlist_type.from_object(object)


@overload
def playlist_from_data(data: PlaylistData) -> Playlist:
    ...


@overload
def playlist_from_data(data: PlaylistData, playlist_type: Type[P]) -> P:
    ...


def playlist_from_data(data: PlaylistData, playlist_type: Type[Playlist] = Playlist) -> Playlist:
    return playlist_type.from_data(data)


def playlist_into_data(playlist: Playlist) -> PlaylistData:
    return playlist.into_data()


from melody.kit.models.track import Track, TrackData
from melody.kit.models.user import User, UserData, user_from_object

PlaylistTracks = List[Track]
PlaylistTracksData = List[TrackData]
