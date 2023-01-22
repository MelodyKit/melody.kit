"""All your music, in one place."""

__description__ = "All your music, in one place."
__url__ = "https://github.com/MelodyKit/melody.web"

__title__ = "kit"
__author__ = "MelodyKit"
__license__ = "MIT"
__version__ = "0.1.0"

from melody.kit import endpoints
from melody.kit.config import Config, ConfigData, get_config
from melody.kit.database import Database
from melody.kit.enums import AlbumType, PrivacyType, URIType
from melody.kit.errors import AuthenticationError, Error, ErrorCode, ErrorData
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
from melody.kit.uri import URI

__all__ = (
    # endpoints
    "endpoints",
    # config
    "Config",
    "ConfigData",
    "get_config",
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
    # errors
    "AuthenticationError",
    "Error",
    "ErrorCode",
    "ErrorData",
    # URI
    "URI",
)
