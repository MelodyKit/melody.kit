"""An API for MelodyKit."""

__description__ = "An API for MelodyKit."
__url__ = "https://github.com/MelodyKit/melody.kit"

__title__ = "kit"
__author__ = "MelodyKit"
__license__ = "MIT"
__version__ = "0.1.0"

from melody.kit.models import Album, Artist, Base, Playlist, Track, User

__all__ = (
    "Base",
    "Track",
    "Artist",
    "Album",
    "Playlist",
    "User",
)
