from enum import Enum

from qrcode.constants import ERROR_CORRECT_L as ERROR_CORRECTION_LOW  # type: ignore
from qrcode.constants import ERROR_CORRECT_M as ERROR_CORRECTION_MEDIUM  # type: ignore
from qrcode.constants import ERROR_CORRECT_Q as ERROR_CORRECTION_QUARTER  # type: ignore
from qrcode.constants import ERROR_CORRECT_H as ERROR_CORRECTION_HIGH  # type: ignore

__all__ = ("AlbumType", "PrivacyType", "EntityType", "LogLevel")


class AlbumType(Enum):
    ALBUM = "album"
    SINGLE = "single"
    COMPILATION = "compilation"

    DEFAULT = ALBUM

    def is_album(self) -> bool:
        return self is type(self).ALBUM

    def is_single(self) -> bool:
        return self is type(self).SINGLE

    def is_compilation(self) -> bool:
        return self is type(self).COMPILATION

    def is_default(self) -> bool:
        return self is type(self).DEFAULT


class PrivacyType(Enum):
    PUBLIC = "public"
    FRIENDS = "friends"
    PRIVATE = "private"

    DEFAULT = PUBLIC

    def is_public(self) -> bool:
        return self is type(self).PUBLIC

    def is_friends(self) -> bool:
        return self is type(self).FRIENDS

    def is_private(self) -> bool:
        return self is type(self).PRIVATE

    def is_default(self) -> bool:
        return self is type(self).DEFAULT


class EntityType(Enum):
    TRACK = "track"
    ARTIST = "artist"
    ALBUM = "album"
    PLAYLIST = "playlist"
    USER = "user"

    def is_track(self) -> bool:
        return self is type(self).TRACK

    def is_artist(self) -> bool:
        return self is type(self).ARTIST

    def is_album(self) -> bool:
        return self is type(self).ALBUM

    def is_playlist(self) -> bool:
        return self is type(self).PLAYLIST

    def is_user(self) -> bool:
        return self is type(self).USER


class LogLevel(Enum):
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"
    TRACE = "trace"


class ErrorCorrection(Enum):
    LOW = "low"
    MEDIUM = "medium"
    QUARTER = "quarter"
    HIGH = "high"

    def into_error_correction(self) -> int:
        return ERROR_CORRECTION[self]  # type: ignore


ERROR_CORRECTION = {
    ErrorCorrection.LOW: ERROR_CORRECTION_LOW,
    ErrorCorrection.MEDIUM: ERROR_CORRECTION_MEDIUM,
    ErrorCorrection.QUARTER: ERROR_CORRECTION_QUARTER,
    ErrorCorrection.HIGH: ERROR_CORRECTION_HIGH,
}
