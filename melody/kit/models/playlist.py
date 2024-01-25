from __future__ import annotations

from typing import List, Optional

from attrs import define, field
from edgedb import Object
from pendulum import DateTime
from typing_extensions import Self
from yarl import URL

from melody.kit.config import CONFIG
from melody.kit.constants import DEFAULT_COUNT, DEFAULT_DURATION
from melody.kit.enums import EntityType, PrivacyType
from melody.kit.links import (
    Linked,
    apple_music_playlist,
    self_playlist,
    spotify_playlist,
    yandex_music_playlist,
)
from melody.kit.models.entity import Entity, EntityData
from melody.kit.models.pagination import Pagination, PaginationData
from melody.kit.uri import URI
from melody.shared.converter import CONVERTER
from melody.shared.date_time import convert_standard_date_time, utc_now
from melody.shared.typing import Data

__all__ = (
    # partial playlists
    "PartialPlaylist",
    "PartialPlaylistData",
    # playlists
    "Playlist",
    "PlaylistData",
    # playlist tracks
    "PlaylistTracks",
    "PlaylistTracksData",
)


class PartialPlaylistData(EntityData):
    uri: str

    follower_count: int

    description: Optional[str]

    duration_ms: int

    track_count: int
    privacy_type: str


@define()
class PartialPlaylist(Entity):
    follower_count: int = field(default=DEFAULT_COUNT)

    description: Optional[str] = field(default=None)

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
    def from_object(cls, object: Object) -> Self:
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
    def from_data(cls, data: PartialPlaylistData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> PartialPlaylistData:
        return CONVERTER.unstructure(self)  # type: ignore


class PlaylistData(PartialPlaylistData):
    user: UserData


@define()
class Playlist(Linked, PartialPlaylist):
    user: User = field()

    follower_count: int = field(default=DEFAULT_COUNT)

    description: Optional[str] = field(default=None)

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
    def from_object(cls, object: Object) -> Self:
        return cls(
            id=object.id,
            name=object.name,
            user=User.from_object(object.user),
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
    def from_data(cls, data: PlaylistData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> PlaylistData:
        return CONVERTER.unstructure(self)  # type: ignore

    @property
    def spotify_url(self) -> Optional[URL]:
        spotify_id = self.spotify_id

        return None if spotify_id is None else URL(spotify_playlist(id=spotify_id))

    @property
    def apple_music_url(self) -> Optional[URL]:
        apple_music_id = self.apple_music_id

        return None if apple_music_id is None else URL(apple_music_playlist(id=apple_music_id))

    @property
    def yandex_music_url(self) -> Optional[URL]:
        yandex_music_id = self.yandex_music_id
        yandex_music_user_id = self.user.yandex_music_id

        return (
            None
            if yandex_music_id is None or yandex_music_user_id is None
            else URL(yandex_music_playlist(user_id=yandex_music_user_id, id=yandex_music_id))
        )

    @property
    def url(self) -> URL:
        return URL(self_playlist(config=CONFIG, id=self.id))


from melody.kit.models.tracks import PositionTrack, PositionTrackData
from melody.kit.models.user import User, UserData


class PlaylistTracksData(Data):
    items: List[PositionTrackData]
    pagination: PaginationData


@define()
class PlaylistTracks:
    items: List[PositionTrack] = field(factory=list)
    pagination: Pagination = field(factory=Pagination)

    @classmethod
    def from_data(cls, data: PlaylistTracksData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> PlaylistTracksData:
        return CONVERTER.unstructure(self)  # type: ignore
