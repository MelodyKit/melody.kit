from typing import Optional, Protocol

from typing_aliases import required
from yarl import URL

__all__ = (
    # linked
    "Linked",
    # spotify links
    "SPOTIFY_ARTIST",
    "SPOTIFY_ALBUM",
    "SPOTIFY_TRACK",
    "SPOTIFY_PLAYLIST",
    "SPOTIFY_USER",
    # apple music links
    "APPLE_MUSIC_ARTIST",
    "APPLE_MUSIC_ALBUM",
    "APPLE_MUSIC_TRACK",
    "APPLE_MUSIC_PLAYLIST",
    "APPLE_MUSIC_USER",
    # yandex music links
    "YANDEX_MUSIC_ARTIST",
    "YANDEX_MUSIC_ALBUM",
    "YANDEX_MUSIC_TRACK",
    "YANDEX_MUSIC_PLAYLIST",
    "YANDEX_MUSIC_USER",
    # spotify
    "spotify_artist",
    "spotify_album",
    "spotify_track",
    "spotify_playlist",
    "spotify_user",
    # apple music
    "apple_music_artist",
    "apple_music_album",
    "apple_music_track",
    "apple_music_playlist",
    "apple_music_user",
    # yandex music
    "yandex_music_artist",
    "yandex_music_album",
    "yandex_music_track",
    "yandex_music_playlist",
    "yandex_music_user",
    # self links
    "SELF_ARTIST",
    "SELF_ALBUM",
    "SELF_TRACK",
    "SELF_PLAYLIST",
    "SELF_USER",
    # self
    "self_artist",
    "self_album",
    "self_track",
    "self_playlist",
    "self_user",
)


class Linked(Protocol):
    @property
    @required
    def spotify_url(self) -> Optional[URL]:
        ...

    @property
    @required
    def apple_music_url(self) -> Optional[URL]:
        ...

    @property
    @required
    def yandex_music_url(self) -> Optional[URL]:
        ...

    @property
    @required
    def url(self) -> URL:
        ...


SPOTIFY_ARTIST = "https://open.spotify.com/artist/{id}"
SPOTIFY_ALBUM = "https://open.spotify.com/album/{id}"
SPOTIFY_TRACK = "https://open.spotify.com/track/{id}"
SPOTIFY_PLAYLIST = "https://open.spotify.com/playlist/{id}"
SPOTIFY_USER = "https://open.spotify.com/user/{id}"

APPLE_MUSIC_ARTIST = "https://music.apple.com/artist/{id}"
APPLE_MUSIC_ALBUM = "https://music.apple.com/album/{id}"
APPLE_MUSIC_TRACK = "https://music.apple.com/album/{album_id}?i={id}"
APPLE_MUSIC_PLAYLIST = "https://music.apple.com/playlist/{id}"
APPLE_MUSIC_USER = "https://music.apple.com/profile/{id}"

YANDEX_MUSIC_ARTIST = "https://music.yandex.com/artist/{id}"
YANDEX_MUSIC_ALBUM = "https://music.yandex.com/album/{id}"
YANDEX_MUSIC_TRACK = "https://music.yandex.com/album/{album_id}/track/{id}"
YANDEX_MUSIC_PLAYLIST = "https://music.yandex.com/users/{user_id}/playlists/{id}"
YANDEX_MUSIC_USER = "https://music.yandex.com/users/{id}"

spotify_artist = SPOTIFY_ARTIST.format
spotify_album = SPOTIFY_ALBUM.format
spotify_track = SPOTIFY_TRACK.format
spotify_playlist = SPOTIFY_PLAYLIST.format
spotify_user = SPOTIFY_USER.format

apple_music_artist = APPLE_MUSIC_ARTIST.format
apple_music_album = APPLE_MUSIC_ALBUM.format
apple_music_track = APPLE_MUSIC_TRACK.format
apple_music_playlist = APPLE_MUSIC_PLAYLIST.format
apple_music_user = APPLE_MUSIC_USER.format

yandex_music_artist = YANDEX_MUSIC_ARTIST.format
yandex_music_album = YANDEX_MUSIC_ALBUM.format
yandex_music_track = YANDEX_MUSIC_TRACK.format
yandex_music_playlist = YANDEX_MUSIC_PLAYLIST.format
yandex_music_user = YANDEX_MUSIC_USER.format

SELF_ARTIST = "https://{config.open}.{config.domain}/artists/{id}"
SELF_ALBUM = "https://{config.open}.{config.domain}/albums/{id}"
SELF_TRACK = "https://{config.open}.{config.domain}/tracks/{id}"
SELF_PLAYLIST = "https://{config.open}.{config.domain}/playlists/{id}"
SELF_USER = "https://{config.open}.{config.domain}/users/{id}"

self_artist = SELF_ARTIST.format
self_album = SELF_ALBUM.format
self_track = SELF_TRACK.format
self_playlist = SELF_PLAYLIST.format
self_user = SELF_USER.format
