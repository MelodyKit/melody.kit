from typing import ClassVar, List, Optional

from attrs import Factory, define
from edgedb import Object
from typing_extensions import Self
from yarl import URL

from melody.kit.config.core import CONFIG
from melody.kit.constants import DEFAULT_COUNT, DEFAULT_DURATION
from melody.kit.enums import EntityType, PrivacyType
from melody.kit.links import (
    Linked,
    apple_music_user,
    self_user,
    spotify_user,
    yandex_music_user,
)
from melody.kit.models.client import Client, ClientData
from melody.kit.models.entity import Entity, EntityData
from melody.kit.models.pagination import Pagination, PaginationData
from melody.kit.uri import Locatable
from melody.shared.converter import CONVERTER
from melody.shared.typing import Data

__all__ = (
    # users
    "User",
    "UserData",
    # user tracks
    "UserTracks",
    "UserTracksData",
    # user albums
    "UserAlbums",
    "UserAlbumsData",
    # user playlists
    "UserPlaylists",
    "UserPlaylistsData",
    # user artists
    "UserArtists",
    "UserArtistsData",
    # user friends
    "UserFriends",
    "UserFriendsData",
    # user followers
    "UserFollowers",
    "UserFollowersData",
    # user following
    "UserFollowing",
    "UserFollowingData",
    # user streams
    "UserStreams",
    "UserStreamsData",
    # user followed playlists
    "UserFollowedPlaylists",
    "UserFollowedPlaylistsData",
)


class UserData(EntityData):
    follower_count: int

    stream_count: int
    stream_duration_ms: int

    privacy_type: str

    discord_id: Optional[str]


@define(kw_only=True)
class User(Linked, Locatable, Entity):
    TYPE: ClassVar[EntityType] = EntityType.USER

    follower_count: int = DEFAULT_COUNT

    stream_count: int = DEFAULT_COUNT
    stream_duration_ms: int = DEFAULT_DURATION

    privacy_type: PrivacyType = PrivacyType.DEFAULT

    discord_id: Optional[str] = None

    @classmethod
    def from_object(cls, object: Object) -> Self:
        self = super().from_object(object)

        self.follower_count = object.follower_count

        self.stream_count = object.stream_count
        self.stream_duration_ms = object.stream_duration_ms

        self.privacy_type = PrivacyType(object.privacy_type.value)

        self.discord_id = object.discord_id

        return self

    @classmethod
    def from_data(cls, data: UserData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserData:
        return CONVERTER.unstructure(self)  # type: ignore

    @property
    def spotify_url(self) -> Optional[URL]:
        spotify_id = self.spotify_id

        return None if spotify_id is None else URL(spotify_user(id=spotify_id))

    @property
    def apple_music_url(self) -> Optional[URL]:
        apple_music_id = self.apple_music_id

        return None if apple_music_id is None else URL(apple_music_user(id=apple_music_id))

    @property
    def yandex_music_url(self) -> Optional[URL]:
        yandex_music_id = self.yandex_music_id

        return None if yandex_music_id is None else URL(yandex_music_user(id=yandex_music_id))

    @property
    def url(self) -> URL:
        return URL(self_user(config=CONFIG, id=self.id))


from melody.kit.models.album import Album, AlbumData
from melody.kit.models.artist import Artist, ArtistData
from melody.kit.models.playlist import Playlist, PlaylistData
from melody.kit.models.streams import Stream, StreamData
from melody.kit.models.tracks import Track, TrackData


class UserTracksData(Data):
    items: List[TrackData]
    pagination: PaginationData


@define()
class UserTracks:
    items: List[Track] = Factory(list)
    pagination: Pagination = Factory(Pagination)

    @classmethod
    def from_data(cls, data: UserTracksData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserTracksData:
        return CONVERTER.unstructure(self)  # type: ignore


class UserAlbumsData(Data):
    items: List[AlbumData]
    pagination: PaginationData


@define()
class UserAlbums:
    items: List[Album] = Factory(list)
    pagination: Pagination = Factory(Pagination)

    @classmethod
    def from_data(cls, data: UserAlbumsData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserAlbumsData:
        return CONVERTER.unstructure(self)  # type: ignore


class UserPlaylistsData(Data):
    items: List[PlaylistData]
    pagination: PaginationData


@define()
class UserPlaylists:
    items: List[Playlist] = Factory(list)
    pagination: Pagination = Factory(Pagination)

    @classmethod
    def from_data(cls, data: UserPlaylistsData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserPlaylistsData:
        return CONVERTER.unstructure(self)  # type: ignore


class UserArtistsData(Data):
    items: List[ArtistData]
    pagination: PaginationData


@define()
class UserArtists:
    items: List[Artist] = Factory(list)
    pagination: Pagination = Factory(Pagination)

    @classmethod
    def from_data(cls, data: UserArtistsData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserArtistsData:
        return CONVERTER.unstructure(self)  # type: ignore


class UserFriendsData(Data):
    items: List[UserData]
    pagination: PaginationData


@define()
class UserFriends:
    items: List[User] = Factory(list)
    pagination: Pagination = Factory(Pagination)

    @classmethod
    def from_data(cls, data: UserFriendsData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserFriendsData:
        return CONVERTER.unstructure(self)  # type: ignore


class UserFollowersData(Data):
    items: List[UserData]
    pagination: PaginationData


@define()
class UserFollowers:
    items: List[User] = Factory(list)
    pagination: Pagination = Factory(Pagination)

    @classmethod
    def from_data(cls, data: UserFollowersData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserFollowersData:
        return CONVERTER.unstructure(self)  # type: ignore


class UserFollowingData(Data):
    items: List[UserData]
    pagination: PaginationData


@define()
class UserFollowing:
    items: List[User] = Factory(list)
    pagination: Pagination = Factory(Pagination)

    @classmethod
    def from_data(cls, data: UserFollowingData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserFollowingData:
        return CONVERTER.unstructure(self)  # type: ignore


class UserStreamsData(Data):
    items: List[StreamData]
    pagination: PaginationData


@define()
class UserStreams:
    items: List[Stream] = Factory(list)
    pagination: Pagination = Factory(Pagination)

    @classmethod
    def from_data(cls, data: UserStreamsData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserStreamsData:
        return CONVERTER.unstructure(self)  # type: ignore


class UserFollowedPlaylistsData(Data):
    items: List[PlaylistData]
    pagination: PaginationData


@define()
class UserFollowedPlaylists:
    items: List[Playlist] = Factory(list)
    pagination: Pagination = Factory(Pagination)

    @classmethod
    def from_data(cls, data: UserFollowedPlaylistsData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserFollowedPlaylistsData:
        return CONVERTER.unstructure(self)  # type: ignore


class UserClientsData(Data):
    items: List[ClientData]
    pagination: PaginationData


@define()
class UserClients:
    items: List[Client] = Factory(list)
    pagination: Pagination = Factory(Pagination)

    @classmethod
    def from_data(cls, data: UserClientsData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserClientsData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]
