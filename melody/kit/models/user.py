from typing import List, Optional, Type, TypeVar, overload

from attrs import define, field
from edgedb import Object  # type: ignore
from pendulum import DateTime
from typing_extensions import TypedDict as Data

from melody.kit.constants import DEFAULT_COUNT, DEFAULT_DURATION
from melody.kit.enums import EntityType, PrivacyType
from melody.kit.models.entity import Entity, EntityData
from melody.kit.models.pagination import Pagination, PaginationData
from melody.kit.uri import URI
from melody.shared.converter import CONVERTER
from melody.shared.date_time import convert_standard_date_time, utc_now

__all__ = (
    # users
    "User",
    "UserData",
    "user_from_object",
    "user_from_data",
    "user_into_data",
    # user tracks
    "UserTracks",
    "UserTracksData",
    "user_tracks_from_data",
    "user_tracks_into_data",
    # user albums
    "UserAlbums",
    "UserAlbumsData",
    "user_albums_from_data",
    "user_albums_into_data",
    # user playlists
    "UserPlaylists",
    "UserPlaylistsData",
    "user_playlists_from_data",
    "user_playlists_into_data",
    # user artists
    "UserArtists",
    "UserArtistsData",
    "user_artists_from_data",
    "user_artists_into_data",
    # user friends
    "UserFriends",
    "UserFriendsData",
    "user_friends_from_data",
    "user_friends_into_data",
    # user followers
    "UserFollowers",
    "UserFollowersData",
    "user_followers_from_data",
    "user_followers_into_data",
    # user following
    "UserFollowing",
    "UserFollowingData",
    "user_following_from_data",
    "user_following_into_data",
    # user streams
    "UserStreams",
    "UserStreamsData",
    "user_streams_from_data",
    "user_streams_into_data",
    # user followed playlists
    "UserFollowedPlaylists",
    "UserFollowedPlaylistsData",
    "user_followed_playlists_from_data",
    "user_followed_playlists_into_data",
)


class UserData(EntityData):
    uri: str

    follower_count: int

    stream_count: int
    stream_duration_ms: int

    privacy_type: str


U = TypeVar("U", bound="User")


@define()
class User(Entity):
    follower_count: int = field(default=DEFAULT_COUNT)

    stream_count: int = field(default=DEFAULT_COUNT)
    stream_duration_ms: int = field(default=DEFAULT_DURATION)

    privacy_type: PrivacyType = field(default=PrivacyType.DEFAULT)

    created_at: DateTime = field(factory=utc_now)

    spotify_id: Optional[str] = field(default=None)
    apple_music_id: Optional[str] = field(default=None)
    yandex_music_id: Optional[str] = field(default=None)

    uri: URI = field()

    @uri.default
    def default_uri(self) -> URI:
        return URI(type=EntityType.USER, id=self.id)

    @classmethod
    def from_object(cls: Type[U], object: Object) -> U:  # type: ignore
        return cls(
            id=object.id,
            name=object.name,
            follower_count=object.follower_count,
            stream_count=object.stream_count,
            stream_duration_ms=object.stream_duration_ms,
            privacy_type=PrivacyType(object.privacy_type.value),
            created_at=convert_standard_date_time(object.created_at),
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
        )

    @classmethod
    def from_data(cls: Type[U], data: UserData) -> U:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def user_from_object(object: Object) -> User:  # type: ignore
    ...


@overload
def user_from_object(object: Object, user_type: Type[U]) -> U:  # type: ignore
    ...


def user_from_object(object: Object, user_type: Type[User] = User) -> User:  # type: ignore
    return user_type.from_object(object)


@overload
def user_from_data(data: UserData) -> User:
    ...


@overload
def user_from_data(data: UserData, user_type: Type[U]) -> U:
    ...


def user_from_data(data: UserData, user_type: Type[User] = User) -> User:
    return user_type.from_data(data)


def user_into_data(user: User) -> UserData:
    return user.into_data()


from melody.kit.models.album import Album, AlbumData
from melody.kit.models.artist import Artist, ArtistData
from melody.kit.models.playlist import PartialPlaylist, PartialPlaylistData, Playlist, PlaylistData
from melody.kit.models.streams import UserStream, UserStreamData
from melody.kit.models.track import Track, TrackData


class UserTracksData(Data):
    items: List[TrackData]
    pagination: PaginationData


UT = TypeVar("UT", bound="UserTracks")


@define()
class UserTracks:
    items: List[Track] = field(factory=list)
    pagination: Pagination = field(factory=Pagination)

    @classmethod
    def from_data(cls: Type[UT], data: UserTracksData) -> UT:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserTracksData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def user_tracks_from_data(data: UserTracksData) -> UserTracks:
    ...


@overload
def user_tracks_from_data(data: UserTracksData, user_tracks_type: Type[UT]) -> UT:
    ...


def user_tracks_from_data(
    data: UserTracksData, user_tracks_type: Type[UserTracks] = UserTracks
) -> UserTracks:
    return user_tracks_type.from_data(data)


def user_tracks_into_data(user_tracks: UserTracks) -> UserTracksData:
    return user_tracks.into_data()


class UserAlbumsData(Data):
    items: List[AlbumData]
    pagination: PaginationData


UA = TypeVar("UA", bound="UserAlbums")


@define()
class UserAlbums:
    items: List[Album] = field(factory=list)
    pagination: Pagination = field(factory=Pagination)

    @classmethod
    def from_data(cls: Type[UA], data: UserAlbumsData) -> UA:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserAlbumsData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def user_albums_from_data(data: UserAlbumsData) -> UserAlbums:
    ...


@overload
def user_albums_from_data(data: UserAlbumsData, user_albums_type: Type[UA]) -> UA:
    ...


def user_albums_from_data(
    data: UserAlbumsData, user_albums_type: Type[UserAlbums] = UserAlbums
) -> UserAlbums:
    return user_albums_type.from_data(data)


def user_albums_into_data(user_albums: UserAlbums) -> UserAlbumsData:
    return user_albums.into_data()


class UserPlaylistsData(Data):
    items: List[PartialPlaylistData]
    pagination: PaginationData


UP = TypeVar("UP", bound="UserPlaylists")


@define()
class UserPlaylists:
    items: List[PartialPlaylist] = field(factory=list)
    pagination: Pagination = field(factory=Pagination)

    @classmethod
    def from_data(cls: Type[UP], data: UserPlaylistsData) -> UP:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserPlaylistsData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def user_playlists_from_data(data: UserPlaylistsData) -> UserPlaylists:
    ...


@overload
def user_playlists_from_data(data: UserPlaylistsData, user_playlists_type: Type[UP]) -> UP:
    ...


def user_playlists_from_data(
    data: UserPlaylistsData, user_playlists_type: Type[UserPlaylists] = UserPlaylists
) -> UserPlaylists:
    return user_playlists_type.from_data(data)


def user_playlists_into_data(user_playlists: UserPlaylists) -> UserPlaylistsData:
    return user_playlists.into_data()


class UserArtistsData(Data):
    items: List[ArtistData]
    pagination: PaginationData


UAT = TypeVar("UAT", bound="UserArtists")


@define()
class UserArtists:
    items: List[Artist] = field(factory=list)
    pagination: Pagination = field(factory=Pagination)

    @classmethod
    def from_data(cls: Type[UAT], data: UserArtistsData) -> UAT:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserArtistsData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def user_artists_from_data(data: UserArtistsData) -> UserArtists:
    ...


@overload
def user_artists_from_data(data: UserArtistsData, user_artists_type: Type[UAT]) -> UAT:
    ...


def user_artists_from_data(
    data: UserArtistsData, user_artists_type: Type[UserArtists] = UserArtists
) -> UserArtists:
    return user_artists_type.from_data(data)


def user_artists_into_data(user_artists: UserArtists) -> UserArtistsData:
    return user_artists.into_data()


class UserFriendsData(Data):
    items: List[UserData]
    pagination: PaginationData


UF = TypeVar("UF", bound="UserFriends")


@define()
class UserFriends:
    items: List[User] = field(factory=list)
    pagination: Pagination = field(factory=Pagination)

    @classmethod
    def from_data(cls: Type[UF], data: UserFriendsData) -> UF:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserFriendsData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def user_friends_from_data(data: UserFriendsData) -> UserFriends:
    ...


@overload
def user_friends_from_data(data: UserFriendsData, user_friends_type: Type[UF]) -> UF:
    ...


def user_friends_from_data(
    data: UserFriendsData, user_friends_type: Type[UserFriends] = UserFriends
) -> UserFriends:
    return user_friends_type.from_data(data)


def user_friends_into_data(user_friends: UserFriends) -> UserFriendsData:
    return user_friends.into_data()


class UserFollowersData(Data):
    items: List[UserData]
    pagination: PaginationData


UFS = TypeVar("UFS", bound="UserFollowers")


@define()
class UserFollowers:
    items: List[User] = field(factory=list)
    pagination: Pagination = field(factory=Pagination)

    @classmethod
    def from_data(cls: Type[UFS], data: UserFollowersData) -> UFS:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserFollowersData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def user_followers_from_data(data: UserFollowersData) -> UserFollowers:
    ...


@overload
def user_followers_from_data(data: UserFollowersData, user_followers_type: Type[UFS]) -> UFS:
    ...


def user_followers_from_data(
    data: UserFollowersData, user_followers_type: Type[UserFollowers] = UserFollowers
) -> UserFollowers:
    return user_followers_type.from_data(data)


def user_followers_into_data(user_followers: UserFollowers) -> UserFollowersData:
    return user_followers.into_data()


class UserFollowingData(Data):
    items: List[UserData]
    pagination: PaginationData


UFG = TypeVar("UFG", bound="UserFollowing")


@define()
class UserFollowing:
    items: List[User] = field(factory=list)
    pagination: Pagination = field(factory=Pagination)

    @classmethod
    def from_data(cls: Type[UFG], data: UserFollowingData) -> UFG:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserFollowingData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def user_following_from_data(data: UserFollowingData) -> UserFollowing:
    ...


@overload
def user_following_from_data(data: UserFollowingData, user_following_type: Type[UFG]) -> UFG:
    ...


def user_following_from_data(
    data: UserFollowingData, user_following_type: Type[UserFollowing] = UserFollowing
) -> UserFollowing:
    return user_following_type.from_data(data)


def user_following_into_data(user_following: UserFollowing) -> UserFollowingData:
    return user_following.into_data()


class UserStreamsData(Data):
    items: List[UserStreamData]
    pagination: PaginationData


US = TypeVar("US", bound="UserStreams")


@define()
class UserStreams:
    items: List[UserStream] = field(factory=list)
    pagination: Pagination = field(factory=Pagination)

    @classmethod
    def from_data(cls: Type[US], data: UserStreamsData) -> US:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserStreamsData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def user_streams_from_data(data: UserStreamsData) -> UserStreams:
    ...


@overload
def user_streams_from_data(data: UserStreamsData, user_streams_type: Type[US]) -> US:
    ...


def user_streams_from_data(
    data: UserStreamsData, user_streams_type: Type[UserStreams] = UserStreams
) -> UserStreams:
    return user_streams_type.from_data(data)


def user_streams_into_data(user_streams: UserStreams) -> UserStreamsData:
    return user_streams.into_data()


class UserFollowedPlaylistsData(Data):
    items: List[PlaylistData]
    pagination: PaginationData


UFP = TypeVar("UFP", bound="UserFollowedPlaylists")


@define()
class UserFollowedPlaylists:
    items: List[Playlist] = field(factory=list)
    pagination: Pagination = field(factory=Pagination)

    @classmethod
    def from_data(cls: Type[UFP], data: UserFollowedPlaylistsData) -> UFP:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserFollowedPlaylistsData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def user_followed_playlists_from_data(data: UserFollowedPlaylistsData) -> UserFollowedPlaylists:
    ...


@overload
def user_followed_playlists_from_data(
    data: UserFollowedPlaylistsData, user_followed_playlists_type: Type[UFP]
) -> UFP:
    ...


def user_followed_playlists_from_data(
    data: UserFollowedPlaylistsData,
    user_followed_playlists_type: Type[UserFollowedPlaylists] = UserFollowedPlaylists,
) -> UserFollowedPlaylists:
    return user_followed_playlists_type.from_data(data)


def user_followed_playlists_into_data(
    user_followed_playlists: UserFollowedPlaylists,
) -> UserFollowedPlaylistsData:
    return user_followed_playlists.into_data()
