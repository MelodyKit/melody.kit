from __future__ import annotations

from datetime import date
from typing import List, Optional
from uuid import UUID

from attrs import define, field

__all__ = ("Base", "Track", "Artist", "Album", "Playlist", "User")


@define()
class Base:
    id: UUID

    name: str

    spotify_id: Optional[str]
    apple_music_id: Optional[int]
    yandex_music_id: Optional[int]


@define()
class Track(Base):
    artists: List[Artist] = field()
    albums: List[Album] = field(factory=list)

    genres: List[str] = field(factory=list)


@define()
class Artist(Base):
    genres: List[str] = field(factory=list)

    tracks: List[Track] = field(factory=list)
    albums: List[Album] = field(factory=list)


@define()
class Album(Base):
    artists: List[Artist]
    tracks: List[Track]

    album_type: str
    release_date: date
    genres: List[str]

    label: str

    track_count: int


@define()
class Playlist(Base):
    user: User = field()
    tracks: List[Track] = field(factory=list)


@define()
class User(Base):
    email: str = field()
    password: str = field()

    playlists: List[Playlist] = field(factory=list)
