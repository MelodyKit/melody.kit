from typing import List, Optional, Type, TypeVar, overload

from attrs import define, field
from edgedb import Object  # type: ignore
from pendulum import DateTime

from melody.kit.constants import DEFAULT_COUNT, DEFAULT_DURATION
from melody.kit.enums import EntityType, PrivacyType
from melody.kit.models.entity import Entity, EntityData
from melody.kit.models.user_stream import UserStream, UserStreamData
from melody.kit.uri import URI
from melody.shared.converter import CONVERTER
from melody.shared.date_time import convert_standard_date_time, utc_now

__all__ = (
    "User",
    "UserData",
    "UserTracks",
    "UserTracksData",
    "UserAlbums",
    "UserAlbumsData",
    "UserPlaylists",
    "UserPlaylistsData",
    "UserArtists",
    "UserArtistsData",
    "UserFriends",
    "UserFriendsData",
    "UserFollowers",
    "UserFollowersData",
    "UserFollowing",
    "UserFollowingData",
    "UserStreams",
    "UserStreamsData",
    "user_from_object",
    "user_from_data",
    "user_into_data",
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
def user_from_object(object: Object) -> User:
    ...


@overload
def user_from_object(object: Object, user_type: Type[U]) -> U:
    ...


def user_from_object(object: Object, user_type: Type[User] = User) -> User:
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
from melody.kit.models.playlist import PartialPlaylist, PartialPlaylistData
from melody.kit.models.track import Track, TrackData

UserTracks = List[Track]
UserTracksData = List[TrackData]

UserAlbums = List[Album]
UserAlbumsData = List[AlbumData]

UserPlaylists = List[PartialPlaylist]
UserPlaylistsData = List[PartialPlaylistData]

UserArtists = List[Artist]
UserArtistsData = List[ArtistData]

UserFriends = List[User]
UserFriendsData = List[UserData]

UserFollowers = List[User]
UserFollowersData = List[UserData]

UserFollowing = List[User]
UserFollowingData = List[UserData]

UserStreams = List[UserStream]
UserStreamsData = List[UserStreamData]
