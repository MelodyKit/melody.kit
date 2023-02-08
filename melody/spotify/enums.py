from enum import Enum

__all__ = ("AlbumType", "EntityType")


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
