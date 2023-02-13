from __future__ import annotations

from enum import Enum

__all__ = (
    "AlbumType",
    "AlbumGroup",
    "RestrictionsReason",
    "DatePrecision",
    "CopyrightType",
    "EntityType",
)


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


class AlbumGroup(Enum):
    ALBUM = "album"
    SINGLE = "single"
    COMPILATION = "compilation"
    APPEARS_ON = "appears_on"

    def is_album(self) -> bool:
        return self is type(self).ALBUM

    def is_single(self) -> bool:
        return self is type(self).SINGLE

    def is_compilation(self) -> bool:
        return self is type(self).COMPILATION

    def is_appears_on(self) -> bool:
        return self is type(self).APPEARS_ON


class RestrictionsReason(Enum):
    MARKET = "market"
    PRODUCT = "product"
    EXPLICIT = "explicit"

    UNKNOWN = "unknown"

    def is_market(self) -> bool:
        return self is type(self).MARKET

    def is_product(self) -> bool:
        return self is type(self).PRODUCT

    def is_explicit(self) -> bool:
        return self is type(self).EXPLICIT

    def is_unknown(self) -> bool:
        return self is type(self).UNKNOWN

    @classmethod
    def _missing_(cls, value: str) -> RestrictionsReason:  # type: ignore
        return cls.UNKNOWN


class CopyrightType(Enum):
    COPYRIGHT = "C"
    PERFORMANCE = "P"

    def is_copyright(self) -> bool:
        return self is type(self).COPYRIGHT

    def is_performance(self) -> bool:
        return self is type(self).PERFORMANCE


class DatePrecision(Enum):
    YEAR = "year"
    MONTH = "month"
    DAY = "day"

    DEFAULT = DAY

    def is_year(self) -> bool:
        return self is type(self).YEAR

    def is_month(self) -> bool:
        return self is type(self).MONTH

    def is_day(self) -> bool:
        return self is type(self).DAY

    def is_default(self) -> bool:
        return self is type(self).DEFAULT


class EntityType(Enum):
    TRACK = "track"
    ARTIST = "artist"
    ALBUM = "album"
    PLAYLIST = "playlist"
    USER = "user"
    SHOW = "show"
    EPISODE = "episode"

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

    def is_show(self) -> bool:
        return self is type(self).SHOW

    def is_episode(self) -> bool:
        return self is type(self).EPISODE
