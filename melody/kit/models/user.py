from typing import List, Optional, Type, TypeVar

from attrs import define, field
from edgedb import Object  # type: ignore
from pendulum import DateTime

from melody.kit.constants import DEFAULT_COUNT, DEFAULT_DURATION
from melody.kit.enums import PrivacyType, URIType
from melody.kit.models.base import Base, BaseData
from melody.kit.models.uri import URIData
from melody.kit.uri import URI
from melody.kit.utils import convert_standard_date_time, utc_now

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
    "user_into_data",
)


class UserData(URIData, BaseData):
    follower_count: int

    stream_count: int
    stream_duration_ms: int

    privacy_type: str


U = TypeVar("U", bound="User")


@define()
class User(Base):
    follower_count: int = field(default=DEFAULT_COUNT)

    stream_count: int = field(default=DEFAULT_COUNT)
    stream_duration_ms: int = field(default=DEFAULT_DURATION)

    privacy_type: PrivacyType = field(default=PrivacyType.DEFAULT)

    created_at: DateTime = field(factory=utc_now)

    spotify_id: Optional[str] = field(default=None)
    apple_music_id: Optional[str] = field(default=None)
    yandex_music_id: Optional[str] = field(default=None)

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

    def into_data(self) -> UserData:
        return UserData(
            id=str(self.id),
            name=self.name,
            created_at=str(self.created_at),
            spotify_id=self.spotify_id,
            apple_music_id=self.apple_music_id,
            yandex_music_id=self.yandex_music_id,
            uri=str(self.uri),
            follower_count=self.follower_count,
            stream_count=self.stream_count,
            stream_duration_ms=self.stream_duration_ms,
            privacy_type=self.privacy_type.value,
        )

    @property
    def uri(self) -> URI:
        return URI(type=URIType.USER, id=self.id)


def user_from_object(object: Object) -> User:
    return User.from_object(object)


def user_into_data(user: User) -> UserData:
    return user.into_data()


from melody.kit.models.album import Album, AlbumData
from melody.kit.models.artist import Artist, ArtistData
from melody.kit.models.playlist import Playlist, PlaylistData
from melody.kit.models.track import Track, TrackData

UserTracks = List[Track]
UserTracksData = List[TrackData]

UserAlbums = List[Album]
UserAlbumsData = List[AlbumData]

UserPlaylists = List[Playlist]
UserPlaylistsData = List[PlaylistData]

UserArtists = List[Artist]
UserArtistsData = List[ArtistData]

UserFriends = List[User]
UserFriendsData = List[UserData]

UserFollowers = List[User]
UserFollowersData = List[UserData]

UserFollowing = List[User]
UserFollowingData = List[UserData]

UserStreams = List[Track]
UserStreamsData = List[TrackData]
