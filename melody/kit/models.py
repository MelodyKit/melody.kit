from __future__ import annotations

from typing import List, Optional, Type, TypeVar
from uuid import UUID

from attrs import define, field
from edgedb import Object  # type: ignore
from iters import iter
from pendulum import Date, DateTime
from typing_extensions import TypedDict

from melody.kit.constants import DEFAULT_COUNT, DEFAULT_EXPLICIT, DEFAULT_ID, DEFAULT_NAME, EMPTY
from melody.kit.date_time_utils import (
    convert_standard_date,
    convert_standard_date_time,
    utc_now,
    utc_today,
)
from melody.kit.enums import AlbumType, PrivacyType, URIType
from melody.kit.uri import URI

__all__ = (
    # models
    "Abstract",
    "Base",
    "Track",
    "Artist",
    "Album",
    "Playlist",
    "User",
    "UserInfo",
    # data
    "AbstractData",
    "BaseData",
    "TrackData",
    "ArtistData",
    "AlbumData",
    "PlaylistData",
    "UserData",
    "UserInfoData",
    # from object
    "abstract_from_object",
    "base_from_object",
    "track_from_object",
    "artist_from_object",
    "album_from_object",
    "playlist_from_object",
    "user_from_object",
    # into data
    "abstract_into_data",
    "base_into_data",
    "track_into_data",
    "artist_into_data",
    "album_into_data",
    "playlist_into_data",
    "user_into_data",
)


class AbstractData(TypedDict):
    id: str


AB = TypeVar("AB", bound="Abstract")


@define()
class Abstract:
    id: UUID

    @classmethod
    def from_object(cls: Type[AB], object: Object) -> AB:  # type: ignore
        return cls(id=object.id)

    def into_data(self) -> AbstractData:
        return AbstractData(id=str(self.id))


def abstract_from_object(object: Object) -> Abstract:
    return Abstract.from_object(object)


def abstract_into_data(abstract: Abstract) -> AbstractData:
    return abstract.into_data()


B = TypeVar("B", bound="Base")


class BaseData(AbstractData):
    name: str

    created_at: str

    spotify_id: Optional[str]
    apple_music_id: Optional[int]
    yandex_music_id: Optional[int]


@define()
class Base(Abstract):
    name: str

    created_at: DateTime = field(factory=utc_now)

    spotify_id: Optional[str] = field(default=None)
    apple_music_id: Optional[int] = field(default=None)
    yandex_music_id: Optional[int] = field(default=None)

    @classmethod
    def default(cls: Type[B]) -> B:
        return cls(id=DEFAULT_ID, name=DEFAULT_NAME)

    @classmethod
    def from_object(cls: Type[B], object: Object) -> B:  # type: ignore
        return cls(
            id=object.id,
            name=object.name,
            created_at=convert_standard_date_time(object.created_at),
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
        )

    def into_data(self) -> BaseData:
        return BaseData(
            id=str(self.id),
            name=self.name,
            created_at=str(self.created_at),
            spotify_id=self.spotify_id,
            apple_music_id=self.apple_music_id,
            yandex_music_id=self.yandex_music_id,
        )


def base_from_object(object: Object) -> Base:
    return Base.from_object(object)


def base_into_data(base: Base) -> BaseData:
    return base.into_data()


class URIData(TypedDict):
    uri: str


class TrackData(URIData, BaseData):
    album: AlbumData
    artists: List[ArtistData]

    explicit: bool

    genres: List[str]


T = TypeVar("T", bound="Track")


@define()
class Track(Base):
    album: Album = field()
    artists: List[Artist] = field()

    explicit: bool = field(default=DEFAULT_EXPLICIT)

    genres: List[str] = field(factory=list)

    created_at: DateTime = field(factory=utc_now)

    spotify_id: Optional[str] = field(default=None)
    apple_music_id: Optional[int] = field(default=None)
    yandex_music_id: Optional[int] = field(default=None)

    @classmethod
    def from_object(cls: Type[T], object: Object) -> T:  # type: ignore
        return cls(
            id=object.id,
            name=object.name,
            album=album_from_object(object.album),
            artists=iter(object.artists).map(artist_from_object).list(),
            explicit=object.explicit,
            created_at=convert_standard_date_time(object.created_at),
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
        )

    def into_data(self) -> TrackData:
        return TrackData(
            id=str(self.id),
            name=self.name,
            created_at=str(self.created_at),
            spotify_id=self.spotify_id,
            apple_music_id=self.apple_music_id,
            yandex_music_id=self.yandex_music_id,
            uri=str(self.uri),
            album=album_into_data(self.album),
            artists=iter(self.artists).map(artist_into_data).list(),
            explicit=self.explicit,
            genres=self.genres,
        )

    @property
    def uri(self) -> URI:
        return URI(type=URIType.TRACK, id=self.id)


def track_from_object(object: Object) -> Track:
    return Track.from_object(object)


def track_into_data(track: Track) -> TrackData:
    return track.into_data()


class ArtistData(URIData, BaseData):
    follower_count: int

    genres: List[str]


AT = TypeVar("AT", bound="Artist")


@define()
class Artist(Base):
    follower_count: int = field(default=DEFAULT_COUNT)

    genres: List[str] = field(factory=list)

    created_at: DateTime = field(factory=utc_now)

    spotify_id: Optional[str] = field(default=None)
    apple_music_id: Optional[int] = field(default=None)
    yandex_music_id: Optional[int] = field(default=None)

    @classmethod
    def from_object(cls: Type[AT], object: Object) -> AT:  # type: ignore
        return cls(
            id=object.id,
            name=object.name,
            follower_count=object.follower_count,
            genres=object.genres,
            created_at=convert_standard_date_time(object.created_at),
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
        )

    def into_data(self) -> ArtistData:
        return ArtistData(
            id=str(self.id),
            name=self.name,
            created_at=str(self.created_at),
            spotify_id=self.spotify_id,
            apple_music_id=self.apple_music_id,
            yandex_music_id=self.yandex_music_id,
            uri=str(self.uri),
            follower_count=self.follower_count,
            genres=self.genres,
        )

    @property
    def uri(self) -> URI:
        return URI(type=URIType.ARTIST, id=self.id)


def artist_from_object(object: Object) -> Artist:
    return Artist.from_object(object)


def artist_into_data(artist: Artist) -> ArtistData:
    return artist.into_data()


class AlbumData(URIData, BaseData):
    artists: List[ArtistData]

    album_type: str
    release_date: str

    track_count: int

    label: Optional[str]

    genres: List[str]


A = TypeVar("A", bound="Album")


@define()
class Album(Base):
    artists: List[Artist] = field()

    album_type: AlbumType = field(default=AlbumType.DEFAULT)
    release_date: Date = field(factory=utc_today)

    track_count: int = field(default=DEFAULT_COUNT)

    label: Optional[str] = field(default=None)

    genres: List[str] = field(factory=list)

    created_at: DateTime = field(factory=utc_now)

    spotify_id: Optional[str] = field(default=None)
    apple_music_id: Optional[int] = field(default=None)
    yandex_music_id: Optional[int] = field(default=None)

    @classmethod
    def from_object(cls: Type[A], object: Object) -> A:  # type: ignore
        return cls(
            id=object.id,
            name=object.name,
            artists=iter(object.artists).map(artist_from_object).list(),
            album_type=AlbumType(object.album_type.value),
            release_date=convert_standard_date(object.release_date),
            track_count=object.track_count,
            genres=object.genres,
            created_at=convert_standard_date_time(object.created_at),
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
        )

    def into_data(self) -> AlbumData:
        return AlbumData(
            id=str(self.id),
            name=self.name,
            created_at=str(self.created_at),
            spotify_id=self.spotify_id,
            apple_music_id=self.apple_music_id,
            yandex_music_id=self.yandex_music_id,
            uri=str(self.uri),
            artists=iter(self.artists).map(artist_into_data).list(),
            album_type=self.album_type.value,
            release_date=str(self.release_date),
            track_count=self.track_count,
            label=self.label,
            genres=self.genres,
        )

    @property
    def uri(self) -> URI:
        return URI(type=URIType.ALBUM, id=self.id)


def album_from_object(object: Object) -> Album:
    return Album.from_object(object)


def album_into_data(album: Album) -> AlbumData:
    return album.into_data()


AlbumTracks = List[Track]
AlbumTracksData = List[TrackData]


class PlaylistData(URIData, BaseData):
    user: UserData

    description: str

    track_count: int
    privacy_type: str


P = TypeVar("P", bound="Playlist")


@define()
class Playlist(Base):
    user: User = field()

    description: str = field(default=EMPTY)

    track_count: int = field(default=DEFAULT_COUNT)

    privacy_type: PrivacyType = field(default=PrivacyType.DEFAULT)

    created_at: DateTime = field(factory=utc_now)

    spotify_id: Optional[str] = field(default=None)
    apple_music_id: Optional[int] = field(default=None)
    yandex_music_id: Optional[int] = field(default=None)

    @classmethod
    def from_object(cls: Type[P], object: Object) -> P:  # type: ignore
        return cls(
            id=object.id,
            name=object.name,
            user=user_from_object(object.user),
            description=object.description,
            track_count=object.track_count,
            privacy_type=PrivacyType(object.privacy_type.value),
            created_at=convert_standard_date_time(object.created_at),
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
        )

    def into_data(self) -> PlaylistData:
        return PlaylistData(
            id=str(self.id),
            name=self.name,
            created_at=str(self.created_at),
            spotify_id=self.spotify_id,
            apple_music_id=self.apple_music_id,
            yandex_music_id=self.yandex_music_id,
            uri=str(self.uri),
            user=user_into_data(self.user),
            description=self.description,
            track_count=self.track_count,
            privacy_type=self.privacy_type.value,
        )

    @property
    def uri(self) -> URI:
        return URI(type=URIType.PLAYLIST, id=self.id)


PlaylistTracks = List[Track]
PlaylistTracksData = List[TrackData]


def playlist_from_object(object: Object) -> Playlist:
    return Playlist.from_object(object)


def playlist_into_data(playlist: Playlist) -> PlaylistData:
    return playlist.into_data()


class UserData(URIData, BaseData):
    follower_count: int

    privacy_type: str


U = TypeVar("U", bound="User")


@define()
class User(Base):
    follower_count: int = field(default=DEFAULT_COUNT)

    privacy_type: PrivacyType = field(default=PrivacyType.DEFAULT)

    created_at: DateTime = field(factory=utc_now)

    spotify_id: Optional[str] = field(default=None)
    apple_music_id: Optional[int] = field(default=None)
    yandex_music_id: Optional[int] = field(default=None)

    @classmethod
    def from_object(cls: Type[U], object: Object) -> U:  # type: ignore
        return cls(
            id=object.id,
            name=object.name,
            follower_count=object.follower_count,
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
            privacy_type=self.privacy_type.value,
        )

    @property
    def uri(self) -> URI:
        return URI(type=URIType.USER, id=self.id)


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


def user_from_object(object: Object) -> User:
    return User.from_object(object)


def user_into_data(user: User) -> UserData:
    return user.into_data()


class UserInfoData(AbstractData):
    verified: bool
    email: str
    password_hash: str


UI = TypeVar("UI", bound="UserInfo")


@define()
class UserInfo(Abstract):
    verified: bool
    email: str
    password_hash: str

    @classmethod
    def from_object(cls: Type[UI], object: Object) -> UI:  # type: ignore
        return cls(
            verified=object.verified,
            id=object.id,
            email=object.email,
            password_hash=object.password_hash,
        )

    def into_data(self) -> UserInfoData:
        return UserInfoData(
            id=str(self.id),
            verified=self.verified,
            email=self.email,
            password_hash=self.password_hash,
        )

    def is_verified(self) -> bool:
        return self.verified


def user_info_from_object(object: Object) -> UserInfo:
    return UserInfo.from_object(object)


def user_info_into_data(user_info: UserInfo) -> UserInfoData:
    return user_info.into_data()
