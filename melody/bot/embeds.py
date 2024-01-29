from typing import Optional

from colors import Color
from discord import Embed
from funcs.application import partial
from iters.iters import iter
from yarl import URL

from melody.bot.colors import color_into_discord, random_melody_color
from melody.bot.constants import INLINE, SEPARATOR
from melody.bot.utils import (
    album_with_url,
    artist_with_url,
    attachment,
    count,
    duration_ms,
    links,
    tick,
)
from melody.kit.models.album import Album
from melody.kit.models.artist import Artist
from melody.kit.models.playlist import Playlist
from melody.kit.models.statistics import Statistics
from melody.kit.models.tracks import Track
from melody.kit.models.user import User

__all__ = (
    "error_embed",
    "not_found_embed",
    "not_linked_embed",
    "inaccessible_embed",
    "album_embed",
    "artist_embed",
    "track_embed",
    "playlist_embed",
    "user_embed",
    "statistics_embed",
)

ERROR_COLOR = Color(0xFF0000)


def error_embed(title: str, description: str, color: Color = ERROR_COLOR) -> Embed:
    return Embed(color=color_into_discord(color), title=title, description=description)


NOT_FOUND = "Not Found"
not_found_embed = partial(error_embed, NOT_FOUND)

NOT_LINKED = "Not Linked"
not_linked_embed = partial(error_embed, NOT_LINKED)

INACCESSIBLE = "Inaccessible"
inaccessible_embed = partial(error_embed, INACCESSIBLE)

ID = "ID"


ARTISTS = "Artists"
TYPE = "Type"
DURATION = "Duration"
TRACKS = "Tracks"
RELEASE_DATE = "Release Date"
LABEL = "Label"
LINKS = "Links"


def album_embed(album: Album, inline: bool = INLINE) -> Embed:
    album_links = links(album)

    embed = (
        Embed(color=color_into_discord(random_melody_color()), title=album.name, url=album.url)
        .add_field(name=ID, value=tick(album.id), inline=inline)
        .add_field(
            name=ARTISTS,
            value=iter(album.artists).map(artist_with_url).join(SEPARATOR),
            inline=inline,
        )
        .add_field(name=TYPE, value=tick(album.album_type.value), inline=inline)
        .add_field(name=TRACKS, value=count(album.track_count), inline=inline)
        .add_field(name=DURATION, value=tick(duration_ms(album.duration_ms)), inline=inline)
        .add_field(name=RELEASE_DATE, value=tick(album.release_date), inline=inline)
        .add_field(name=LABEL, value=album.label, inline=inline)
    )

    if album_links:
        embed = embed.add_field(name=LINKS, value=album_links, inline=inline)

    return embed


FOLLOWERS = "Followers"
STREAMS = "Streams"


def artist_embed(artist: Artist, inline: bool = INLINE) -> Embed:
    artist_links = links(artist)

    embed = (
        Embed(color=color_into_discord(random_melody_color()), title=artist.name, url=artist.url)
        .add_field(name=ID, value=tick(artist.id), inline=inline)
        .add_field(name=FOLLOWERS, value=count(artist.follower_count), inline=inline)
        .add_field(name=STREAMS, value=count(artist.stream_count), inline=inline)
    )

    if artist_links:
        embed = embed.add_field(name=LINKS, value=artist_links, inline=inline)

    return embed


ALBUM = "Album"


def track_embed(track: Track, inline: bool = INLINE) -> Embed:
    track_links = links(track)

    embed = (
        Embed(color=color_into_discord(random_melody_color()), title=track.name, url=track.url)
        .add_field(name=ID, value=tick(track.id), inline=inline)
        .add_field(
            name=ARTISTS,
            value=iter(track.artists).map(artist_with_url).join(SEPARATOR),
            inline=inline,
        )
        .add_field(name=ALBUM, value=album_with_url(track.album), inline=inline)
        .add_field(name=DURATION, value=tick(duration_ms(track.duration_ms)), inline=inline)
        .add_field(name=STREAMS, value=count(track.stream_count), inline=inline)
    )

    if track_links:
        embed = embed.add_field(name=LINKS, value=track_links, inline=inline)

    return embed


PRIVACY_TYPE = "Privacy Type"
USER = "User"


def playlist_embed(
    playlist: Playlist, image_url: Optional[URL] = None, inline: bool = INLINE
) -> Embed:
    playlist_links = links(playlist)

    embed = (
        Embed(
            color=color_into_discord(random_melody_color()),
            title=playlist.name,
            url=playlist.url,
            description=playlist.description,
        )
        .add_field(name=ID, value=tick(playlist.id), inline=inline)
        .add_field(name=PRIVACY_TYPE, value=tick(playlist.privacy_type.value), inline=inline)
        .add_field(name=FOLLOWERS, value=count(playlist.follower_count), inline=inline)
        .add_field(name=TRACKS, value=count(playlist.track_count), inline=inline)
        .add_field(name=DURATION, value=tick(duration_ms(playlist.duration_ms)), inline=inline)
    )

    if playlist_links:
        embed = embed.add_field(name=LINKS, value=playlist_links, inline=inline)

    if image_url is None:
        return embed

    return embed.set_image(url=image_url)


def user_embed(user: User, image_url: Optional[URL] = None, inline: bool = INLINE) -> Embed:
    user_links = links(user)

    embed = (
        Embed(color=color_into_discord(random_melody_color()), title=user.name, url=user.url)
        .add_field(name=ID, value=tick(user.id), inline=inline)
        .add_field(name=PRIVACY_TYPE, value=tick(user.privacy_type.value), inline=inline)
        .add_field(name=FOLLOWERS, value=count(user.follower_count), inline=inline)
        .add_field(name=STREAMS, value=count(user.stream_count), inline=inline)
    )

    if user_links:
        embed = embed.add_field(name=LINKS, value=user_links, inline=inline)

    if image_url is None:
        return embed

    return embed.set_image(url=image_url)


STATISTICS = "Statistics"
USERS = "Users"
ALBUMS = "Albums"
PLAYLISTS = "Playlists"


def statistics_embed(statistics: Statistics, inline: bool = INLINE) -> Embed:
    return (
        Embed(color=color_into_discord(random_melody_color()), title=STATISTICS)
        .add_field(name=USERS, value=count(statistics.user_count), inline=inline)
        .add_field(name=STREAMS, value=count(statistics.stream_count), inline=inline)
        .add_field(name=TRACKS, value=count(statistics.track_count), inline=inline)
        .add_field(name=ARTISTS, value=count(statistics.artist_count), inline=inline)
        .add_field(name=ALBUMS, value=count(statistics.album_count), inline=inline)
        .add_field(name=PLAYLISTS, value=count(statistics.playlist_count), inline=inline)
    )
