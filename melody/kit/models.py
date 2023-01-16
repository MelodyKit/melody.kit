from __future__ import annotations

from typing import List, Optional, Type, TypeVar
from uuid import UUID

from attrs import define, field
from edgedb import Object  # type: ignore
from iters import iter
from pendulum import Date, DateTime
from typing_extensions import TypedDict

from melody.kit.defaults import DEFAULT_COUNT, DEFAULT_EXPLICIT, DEFAULT_ID, DEFAULT_NAME
from melody.kit.enums import AlbumType
from melody.kit.utils import convert_standard_date, convert_standard_date_time, utc_now, utc_today

__all__ = (
    "Base",
    "PartialTrack",
    "Track",
    "PartialArtist",
    "Artist",
    "PartialAlbum",
    "Album",
    "PartialPlaylist",
    "Playlist",
    "PartialUser",
    "User",
)


B = TypeVar("B", bound="Base")


class BaseData(TypedDict):
    id: str

    name: str

    created_at: str

    spotify_id: Optional[str]
    apple_music_id: Optional[int]
    yandex_music_id: Optional[int]


@define()
class Base:
    id: UUID

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


class PartialTrackData(BaseData):
    artists: List[PartialArtistData]

    explicit: bool


PT = TypeVar("PT", bound="PartialTrack")


@define()
class PartialTrack(Base):
    artists: List[PartialArtist]

    explicit: bool = field(default=DEFAULT_EXPLICIT)

    created_at: DateTime = field(factory=utc_now)

    spotify_id: Optional[str] = field(default=None)
    apple_music_id: Optional[int] = field(default=None)
    yandex_music_id: Optional[int] = field(default=None)

    @classmethod
    def from_object(cls: Type[PT], object: Object) -> PT:  # type: ignore
        return cls(
            id=object.id,
            name=object.name,
            artists=iter(object.artists).map(partial_artist_from_object).list(),
            explicit=object.explicit,
            created_at=convert_standard_date_time(object.created_at),
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
        )

    def into_data(self) -> PartialTrackData:
        return PartialTrackData(
            id=str(self.id),
            name=self.name,
            created_at=str(self.created_at),
            spotify_id=self.spotify_id,
            apple_music_id=self.apple_music_id,
            yandex_music_id=self.yandex_music_id,
            artists=iter(self.artists).map(partial_artist_into_data).list(),
            explicit=self.explicit,
        )


def partial_track_from_object(object: Object) -> PartialTrack:
    return PartialTrack.from_object(object)


def partial_track_into_data(partial_track: PartialTrack) -> PartialTrackData:
    return partial_track.into_data()


class TrackData(PartialTrackData):
    album: PartialAlbumData

    genres: List[str]


T = TypeVar("T", bound="Track")


@define()
class Track(PartialTrack):
    album: PartialAlbum

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
            artists=iter(object.artists).map(partial_artist_from_object).list(),
            explicit=object.explicit,
            album=partial_album_from_object(object.album),
            genres=object.genres,
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
            artists=iter(self.artists).map(partial_artist_into_data).list(),
            explicit=self.explicit,
            album=partial_album_into_data(self.album),
            genres=self.genres,
        )


def track_from_object(object: Object) -> Track:
    return Track.from_object(object)


def track_into_data(track: Track) -> TrackData:
    return track.into_data()


class PartialArtistData(BaseData):
    pass


@define()
class PartialArtist(Base):
    pass


def partial_artist_from_object(object: Object) -> PartialArtist:
    return PartialArtist.from_object(object)


def partial_artist_into_data(partial_artist: PartialArtist) -> PartialArtistData:
    return partial_artist.into_data()


class ArtistData(PartialArtistData):
    genres: List[str]

    tracks: List[PartialTrackData]
    albums: List[PartialAlbumData]


AT = TypeVar("AT", bound="Artist")


@define()
class Artist(PartialArtist):
    genres: List[str] = field(factory=list)

    tracks: List[PartialTrack] = field(factory=list)
    albums: List[PartialAlbum] = field(factory=list)

    created_at: DateTime = field(factory=utc_now)

    spotify_id: Optional[str] = field(default=None)
    apple_music_id: Optional[int] = field(default=None)
    yandex_music_id: Optional[int] = field(default=None)

    @classmethod
    def from_object(cls: Type[AT], object: Object) -> AT:  # type: ignore
        return cls(
            id=object.id,
            name=object.name,
            genres=object.genres,
            tracks=iter(object.tracks).map(partial_track_from_object).list(),
            albums=iter(object.albums).map(partial_album_from_object).list(),
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
            genres=self.genres,
            tracks=iter(self.tracks).map(partial_track_into_data).list(),
            albums=iter(self.albums).map(partial_album_into_data).list(),
        )


def artist_from_object(object: Object) -> Artist:
    return Artist.from_object(object)


def artist_into_data(artist: Artist) -> ArtistData:
    return artist.into_data()


class PartialAlbumData(BaseData):
    album_type: str
    release_date: str

    track_count: int


PA = TypeVar("PA", bound="PartialAlbum")


@define()
class PartialAlbum(Base):
    album_type: AlbumType = field(default=AlbumType.ALBUM)
    release_date: Date = field(factory=utc_today)

    track_count: int = field(default=DEFAULT_COUNT)

    created_at: DateTime = field(factory=utc_now)

    spotify_id: Optional[str] = field(default=None)
    apple_music_id: Optional[int] = field(default=None)
    yandex_music_id: Optional[int] = field(default=None)

    @classmethod
    def from_object(cls: Type[PA], object: Object) -> PA:  # type: ignore
        return cls(
            id=object.id,
            name=object.name,
            album_type=AlbumType(object.album_type.value),
            release_date=convert_standard_date(object.release_date),
            track_count=object.track_count,
            created_at=convert_standard_date_time(object.created_at),
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
        )

    def into_data(self) -> PartialAlbumData:
        return PartialAlbumData(
            id=str(self.id),
            name=self.name,
            created_at=str(self.created_at),
            spotify_id=self.spotify_id,
            apple_music_id=self.apple_music_id,
            yandex_music_id=self.yandex_music_id,
            album_type=self.album_type.value,
            release_date=str(self.release_date),
            track_count=self.track_count,
        )


def partial_album_from_object(object: Object) -> PartialAlbum:
    return PartialAlbum.from_object(object)


def partial_album_into_data(partial_album: PartialAlbum) -> PartialAlbumData:
    return partial_album.into_data()


class AlbumData(PartialAlbumData):
    label: str

    genres: List[str]

    artists: List[PartialArtistData]
    tracks: List[PartialTrackData]


A = TypeVar("A", bound="Album")


@define()
class Album(PartialAlbum):
    label: str = field()

    artists: List[PartialArtist] = field()
    tracks: List[PartialTrack] = field()

    album_type: AlbumType = field(default=AlbumType.ALBUM)
    release_date: Date = field(factory=utc_today)

    track_count: int = field(default=DEFAULT_COUNT)

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
            album_type=AlbumType(object.album_type.value),
            release_date=object.release_date,
            track_count=object.track_count,
            label=object.label,
            genres=object.genres,
            artists=iter(object.artists).map(partial_artist_from_object).list(),
            tracks=iter(object.tracks).map(partial_track_from_object).list(),
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
            album_type=self.album_type.value,
            release_date=str(self.release_date),
            track_count=self.track_count,
            label=self.label,
            genres=self.genres,
            artists=iter(self.artists).map(partial_artist_into_data).list(),
            tracks=iter(self.tracks).map(partial_track_into_data).list(),
        )


def album_from_object(object: Object) -> Album:
    return Album.from_object(object)


def album_into_data(album: Album) -> AlbumData:
    return album.into_data()


class PartialPlaylistData(BaseData):
    tracks: List[TrackData]


PP = TypeVar("PP", bound="PartialPlaylist")


@define()
class PartialPlaylist(Base):
    tracks: List[Track] = field(factory=list)

    created_at: DateTime = field(factory=utc_now)

    spotify_id: Optional[str] = field(default=None)
    apple_music_id: Optional[int] = field(default=None)
    yandex_music_id: Optional[int] = field(default=None)

    @classmethod
    def from_object(cls: Type[PP], object: Object) -> PP:  # type: ignore
        return cls(
            id=object.id,
            name=object.name,
            tracks=iter(object.tracks).map(track_from_object).list(),
            created_at=convert_standard_date_time(object.created_at),
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
        )

    def into_data(self) -> PartialPlaylistData:
        return PartialPlaylistData(
            id=str(self.id),
            name=self.name,
            created_at=str(self.created_at),
            spotify_id=self.spotify_id,
            apple_music_id=self.apple_music_id,
            yandex_music_id=self.yandex_music_id,
            tracks=iter(self.tracks).map(track_into_data).list(),
        )


def partial_playlist_from_object(object: Object) -> PartialPlaylist:
    return PartialPlaylist.from_object(object)


def partial_playlist_into_data(partial_playlist: PartialPlaylist) -> PartialPlaylistData:
    return partial_playlist.into_data()


class PlaylistData(PartialPlaylistData):
    user: PartialUserData


P = TypeVar("P", bound="Playlist")


@define()
class Playlist(PartialPlaylist):
    user: PartialUser = field()
    tracks: List[Track] = field(factory=list)

    created_at: DateTime = field(factory=utc_now)

    spotify_id: Optional[str] = field(default=None)
    apple_music_id: Optional[int] = field(default=None)
    yandex_music_id: Optional[int] = field(default=None)

    @classmethod
    def from_object(cls: Type[P], object: Object) -> P:  # type: ignore
        return cls(
            id=object.id,
            name=object.name,
            created_at=convert_standard_date_time(object.created_at),
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
            user=partial_user_from_object(object.user),
            tracks=iter(object.tracks).map(track_from_object).list(),
        )

    def into_data(self) -> PlaylistData:
        return PlaylistData(
            id=str(self.id),
            name=self.name,
            created_at=str(self.created_at),
            spotify_id=self.spotify_id,
            apple_music_id=self.apple_music_id,
            yandex_music_id=self.yandex_music_id,
            tracks=iter(self.tracks).map(track_into_data).list(),
            user=partial_user_into_data(self.user),
        )


def playlist_from_object(object: Object) -> Playlist:
    return Playlist.from_object(object)


def playlist_into_data(playlist: Playlist) -> PlaylistData:
    return playlist.into_data()


class PartialUserData(BaseData):
    pass


@define()
class PartialUser(Base):
    pass


def partial_user_from_object(object: Object) -> PartialUser:
    return PartialUser.from_object(object)


def partial_user_into_data(partial_user: PartialUser) -> PartialUserData:
    return partial_user.into_data()


class UserData(PartialUserData):
    tracks: List[TrackData]
    albums: List[AlbumData]
    artists: List[PartialArtistData]
    playlists: List[PartialPlaylistData]


U = TypeVar("U", bound="User")


@define()
class User(PartialUser):
    tracks: List[Track] = field(factory=list)
    albums: List[Album] = field(factory=list)
    artists: List[PartialArtist] = field(factory=list)
    playlists: List[PartialPlaylist] = field(factory=list)

    created_at: DateTime = field(factory=utc_now)

    spotify_id: Optional[str] = field(default=None)
    apple_music_id: Optional[int] = field(default=None)
    yandex_music_id: Optional[int] = field(default=None)

    @classmethod
    def from_object(cls: Type[U], object: Object) -> U:  # type: ignore
        return cls(
            id=object.id,
            name=object.name,
            tracks=iter(object.tracks).map(track_from_object).list(),
            albums=iter(object.albums).map(album_from_object).list(),
            artists=iter(object.artists).map(partial_artist_from_object).list(),
            playlists=iter(object.playlists).map(partial_playlist_from_object).list(),
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
            tracks=iter(self.tracks).map(track_into_data).list(),
            albums=iter(self.albums).map(album_into_data).list(),
            artists=iter(self.artists).map(partial_artist_into_data).list(),
            playlists=iter(self.playlists).map(partial_playlist_into_data).list(),
        )


def user_from_object(object: Object) -> User:
    return User.from_object(object)


def user_into_data(user: User) -> UserData:
    return user.into_data()
