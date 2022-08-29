from __future__ import annotations

from datetime import date
from typing import List, Optional, Type, TypeVar
from uuid import UUID

from edgedb import Object

from attrs import define, field

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


@define()
class Base:
    id: UUID

    name: str

    spotify_id: Optional[str]
    apple_music_id: Optional[int]
    yandex_music_id: Optional[int]

    @classmethod
    def from_object(cls: Type[B], object: Object) -> B:
        return cls(
            id=object.id,
            name=object.name,
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
        )


PT = TypeVar("PT", bound="PartialTrack")


@define()
class PartialTrack(Base):
    artists: List[PartialArtist]

    @classmethod
    def from_object(cls: Type[PT], object: Object) -> PT:
        return cls(
            id=object.id,
            name=object.name,
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
            artists=[PartialArtist.from_object(artist) for artist in object.artists],
        )


T = TypeVar("T", bound="Track")


@define()
class Track(PartialTrack):
    albums: List[PartialAlbum] = field(factory=list)

    genres: List[str] = field(factory=list)

    @classmethod
    def from_object(cls: Type[T], object: Object) -> T:
        return cls(
            id=object.id,
            name=object.name,
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
            artists=list(map(PartialArtist.from_object, object.artists)),
            albums=list(map(PartialAlbum.from_object, object.albums)),
            genres=object.genres,
        )


@define()
class PartialArtist(Base):
    pass


AT = TypeVar("AT", bound="Artist")


@define()
class Artist(PartialArtist):
    genres: List[str] = field(factory=list)

    tracks: List[PartialTrack] = field(factory=list)
    albums: List[PartialAlbum] = field(factory=list)

    @classmethod
    def from_object(cls: Type[AT], object: Object) -> AT:
        return cls(
            id=object.id,
            name=object.name,
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
            genres=object.genres,
            tracks=list(map(PartialTrack.from_object, object.tracks)),
            albums=list(map(PartialAlbum.from_object, object.albums)),
        )


PA = TypeVar("PA", bound="PartialAlbum")


@define()
class PartialAlbum(Base):
    album_type: str
    release_date: date

    track_count: int

    @classmethod
    def from_object(cls: Type[PA], object: Object) -> PA:
        return cls(
            id=object.id,
            name=object.name,
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
            album_type=object.album_type,
            release_date=object.release_date,
            track_count=object.track_count,
        )


A = TypeVar("A", bound="Album")


@define()
class Album(PartialAlbum):
    label: str

    genres: List[str]

    artists: List[PartialArtist]
    tracks: List[PartialTrack]

    @classmethod
    def from_object(cls: Type[A], object: Object) -> A:
        return cls(
            id=object.id,
            name=object.name,
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
            album_type=object.album_type,
            release_date=object.release_date,
            track_count=object.track_count,
            label=object.label,
            genres=object.genres,
            artists=list(map(PartialArtist.from_object, object.artists)),
            tracks=list(map(PartialTrack.from_object, object.tracks)),
        )


PP = TypeVar("PP", bound="PartialPlaylist")


@define()
class PartialPlaylist(Base):
    tracks: List[Track] = field(factory=list)

    @classmethod
    def from_object(cls: Type[PP], object: Object) -> PP:
        return cls(
            id=object.id,
            name=object.name,
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
            tracks=list(map(Track.from_object, object.tracks)),
        )


P = TypeVar("P", bound="Playlist")


@define()
class Playlist(Base):
    user: PartialUser = field()
    tracks: List[Track] = field(factory=list)

    @classmethod
    def from_object(cls: Type[P], object: Object) -> P:
        return cls(
            id=object.id,
            name=object.name,
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
            user=PartialUser.from_object(object.user),
            tracks=list(map(Track.from_object, object.tracks)),
        )


@define()
class PartialUser(Base):
    pass


U = TypeVar("U", bound="User")


@define()
class User(PartialUser):
    tracks: List[Track] = field(factory=list)
    albums: List[Album] = field(factory=list)
    playlists: List[PartialPlaylist] = field(factory=list)

    @classmethod
    def from_object(cls: Type[U], object: Object) -> U:
        return cls(
            id=object.id,
            name=object.name,
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
            tracks=list(map(Track.from_object, object.tracks)),
            albums=list(map(Album.from_object, object.albums)),
            playlists=list(map(PartialPlaylist.from_object, object.playlists)),
        )
