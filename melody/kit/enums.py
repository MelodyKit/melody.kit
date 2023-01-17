from enum import Enum

__all__ = ("AlbumType",)


class AlbumType(Enum):
    ALBUM = "album"
    SINGLE = "single"
    COMPILATION = "compilation"

    DEFAULT = ALBUM


class PrivacyType(Enum):
    PUBLIC = "public"
    FRIENDS = "friends"
    PRIVATE = "private"

    DEFAULT = PUBLIC
