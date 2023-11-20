from __future__ import annotations

from typing import List, Optional, Type
from typing import TypedDict as Data
from typing import TypeVar, overload

from attrs import define, field
from edgedb import Object  # type: ignore
from pendulum import DateTime

from melody.kit.constants import DEFAULT_COUNT, DEFAULT_DURATION
from melody.kit.enums import EntityType, PrivacyType
from melody.kit.models.entity import Entity, EntityData
from melody.kit.models.pagination import Pagination, PaginationData
from melody.kit.uri import URI
from melody.shared.constants import EMPTY
from melody.shared.converter import CONVERTER
from melody.shared.date_time import convert_standard_date_time, utc_now

__all__ = (
    # partial playlists
    "PartialPlaylist",
    "PartialPlaylistData",
    "partial_playlist_from_object",
    "partial_playlist_from_data",
    "partial_playlist_into_data",
    # playlists
    "Playlist",
    "PlaylistData",
    "playlist_from_object",
    "playlist_from_data",
    "playlist_into_data",
    # playlist tracks
    "PlaylistTracks",
    "PlaylistTracksData",
    "playlist_tracks_from_data",
    "playlist_tracks_into_data",
)


class PartialPlaylistData(EntityData):
    uri: str

    follower_count: int

    description: str

    duration_ms: int

    track_count: int
    privacy_type: str


Q = TypeVar("Q", bound="PartialPlaylist")


@define()
class PartialPlaylist(Entity):
    follower_count: int = field(default=DEFAULT_COUNT)

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
            follower_count=object.follower_count,
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
def partial_playlist_from_object(object: Object) -> PartialPlaylist:  # type: ignore
    ...


@overload
def partial_playlist_from_object(  # type: ignore
    object: Object, partial_playlist_type: Type[Q]
) -> Q:
    ...


def partial_playlist_from_object(
    object: Object, partial_playlist_type: Type[PartialPlaylist] = PartialPlaylist  # type: ignore
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


class PlaylistData(PartialPlaylistData):
    user: UserData


P = TypeVar("P", bound="Playlist")


@define()
class Playlist(PartialPlaylist):
    user: User = field()

    follower_count: int = field(default=DEFAULT_COUNT)

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
            follower_count=object.follower_count,
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
def playlist_from_object(object: Object) -> Playlist:  # type: ignore
    ...


@overload
def playlist_from_object(object: Object, playlist_type: Type[P]) -> P:  # type: ignore
    ...


def playlist_from_object(
    object: Object, playlist_type: Type[Playlist] = Playlist  # type: ignore
) -> Playlist:
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


from melody.kit.models.track import PositionTrack, PositionTrackData
from melody.kit.models.user import User, UserData, user_from_object


class PlaylistTracksData(Data):
    items: List[PositionTrackData]
    pagination: PaginationData


PT = TypeVar("PT", bound="PlaylistTracks")


@define()
class PlaylistTracks:
    items: List[PositionTrack] = field(factory=list)
    pagination: Pagination = field(factory=Pagination)

    @classmethod
    def from_data(cls: Type[PT], data: PlaylistTracksData) -> PT:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> PlaylistTracksData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def playlist_tracks_from_data(data: PlaylistTracksData) -> PlaylistTracks:
    ...


@overload
def playlist_tracks_from_data(data: PlaylistTracksData, playlist_tracks_type: Type[PT]) -> PT:
    ...


def playlist_tracks_from_data(
    data: PlaylistTracksData, playlist_tracks_type: Type[PlaylistTracks] = PlaylistTracks
) -> PlaylistTracks:
    return playlist_tracks_type.from_data(data)


def playlist_tracks_into_data(playlist_tracks: PlaylistTracks) -> PlaylistTracksData:
    return playlist_tracks.into_data()
