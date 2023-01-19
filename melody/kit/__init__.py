"""An API for MelodyKit."""

__description__ = "An API for MelodyKit."
__url__ = "https://github.com/MelodyKit/melody.kit"

__title__ = "kit"
__author__ = "MelodyKit"
__license__ = "MIT"
__version__ = "0.1.0"

from melody.kit.albums import get_album
from melody.kit.authentication import login, logout, register
from melody.kit.database import Database
from melody.kit.models import (
    Album,
    Artist,
    Base,
    PartialAlbum,
    PartialArtist,
    PartialPlaylist,
    PartialTrack,
    PartialUser,
    Playlist,
    Track,
    User,
)
from melody.kit.tracks import get_track

__all__ = (
    # database
    "Database",
    # models
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
    # endpoints
    # albums
    "get_album",
    # authentication
    "login",
    "logout",
    "register",
    # tracks
    "get_track",
)
