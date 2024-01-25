from melody.bot.constants import (
    ATTACHMENT,
    BULLET,
    COUNT,
    HOURS_TO_MINUTES,
    HUMAN_DURATION,
    MILLISECONDS_TO_SECONDS,
    NEW_LINE,
    SECONDS_TO_MINUTES,
    TICK,
    WITH_URL,
)
from melody.kit.links import Linked
from melody.kit.models.album import Album
from melody.kit.models.artist import Artist
from melody.kit.models.playlist import Playlist
from melody.kit.models.tracks import Track
from melody.kit.models.user import User

__all__ = (
    "attachment",
    "count",
    "bullet",
    "concat_new_line",
    "with_url",
    "artist_with_url",
    "album_with_url",
    "track_with_url",
    "playlist_with_url",
    "user_with_url",
    "links",
    "duration_ms",
)

attachment = ATTACHMENT.format

count = COUNT.format

bullet = BULLET.format

concat_new_line = NEW_LINE.join

tick = TICK.format

with_url = WITH_URL.format


def artist_with_url(artist: Artist) -> str:
    return with_url(content=artist.name, url=artist.url)


def album_with_url(album: Album) -> str:
    return with_url(content=album.name, url=album.url)


def track_with_url(track: Track) -> str:
    return with_url(content=track.name, url=track.url)


def playlist_with_url(playlist: Playlist) -> str:
    return with_url(content=playlist.name, url=playlist.url)


def user_with_url(user: User) -> str:
    return with_url(content=user.name, url=user.url)


SPOTIFY = "Spotify"
APPLE_MUSIC = "Apple Music"
YANDEX_MUSIC = "Yandex Music"


def links(linked: Linked) -> str:
    mapping = {
        SPOTIFY: linked.spotify_url,
        APPLE_MUSIC: linked.apple_music_url,
        YANDEX_MUSIC: linked.yandex_music_url,
    }

    result = (
        bullet(with_url(content=name, url=url)) for name, url in mapping.items() if url is not None
    )

    return concat_new_line(result)


human_duration = HUMAN_DURATION.format


def duration_ms(total_milliseconds: int) -> str:
    total_seconds, milliseconds = divmod(total_milliseconds, MILLISECONDS_TO_SECONDS)
    total_minutes, seconds = divmod(total_seconds, SECONDS_TO_MINUTES)
    hours, minutes = divmod(total_minutes, HOURS_TO_MINUTES)

    return human_duration(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)
