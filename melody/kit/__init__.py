"""An API for MelodyKit."""

__description__ = "An API for MelodyKit."
__url__ = "https://github.com/MelodyKit/melody.kit"

__title__ = "kit"
__author__ = "MelodyKit"
__license__ = "MIT"
__version__ = "0.1.0"

from melody.kit.albums import get_album, get_album_link, get_album_tracks
from melody.kit.artists import get_artist, get_artist_link
from melody.kit.authentication import login, logout, register
from melody.kit.database import Database
from melody.kit.enums import AlbumType, PrivacyType, URIType
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
from melody.kit.playlists import get_playlist, get_playlist_link, get_playlist_tracks
from melody.kit.tracks import get_track, get_track_link
from melody.kit.uri import URI
from melody.kit.users import get_self, get_self_link, get_user, get_user_link

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
    "URIType",
    # URI
    "URI",
    # endpoints
    # albums
    "get_album",
    "get_album_link",
    "get_album_tracks",
    # artists
    "get_artist",
    "get_artist_link",
    # authentication
    "login",
    "logout",
    "register",
    # playlists
    "get_playlist",
    "get_playlist_link",
    "get_playlist_tracks",
    # tracks
    "get_track",
    "get_track_link",
    # users
    "get_self",
    "get_self_link",
    "get_user",
    "get_user_link",
)
