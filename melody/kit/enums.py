from enum import Enum

__all__ = ("AlbumType", "PrivacyType")


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
