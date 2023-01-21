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
from melody.kit.enums import AlbumType, PrivacyType
from melody.kit.models import (
    Abstract,
    AbstractData,
    Album,
    AlbumData,
    Artist,
    ArtistData,
    Base,
    BaseData,
    Playlist,
    PlaylistData,
    Track,
    TrackData,
    User,
    UserData,
)
from melody.kit.playlists import get_playlist
from melody.kit.tracks import get_track
from melody.kit.users import get_self, get_user

__all__ = (
    # database
    "Database",
    # models
    "Abstract",
    "Base",
    "Track",
    "Artist",
    "Album",
    "Playlist",
    "User",
    # data
    "AbstractData",
    "BaseData",
    "ArtistData",
    "TrackData",
    "ArtistData",
    "AlbumData",
    "PlaylistData",
    "UserData",
    # enums
    "AlbumType",
    "PrivacyType",
    # endpoints
    # albums
    "get_album",
    # authentication
    "login",
    "logout",
    "register",
    # playlists
    "get_playlist",
    # tracks
    "get_track",
    # users
    "get_self",
    "get_user",
)
