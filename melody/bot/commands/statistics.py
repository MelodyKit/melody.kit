from discord import Embed, Interaction

from melody.bot.colors import color_into_discord, random_melody_color
from melody.bot.constants import INLINE
from melody.bot.core import Melody, client
from melody.kit.core import database
from melody.kit.models.statistics import Statistics

__all__ = ("get_statistics",)

COUNT = "{:,}"
count = COUNT.format

STATISTICS = "Statistics"
USERS = "Users"
STREAMS = "Streams"
TRACKS = "Tracks"
ARTISTS = "Artists"
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


@client.tree.command(name="statistics", description="Fetches overall statistics.")
async def get_statistics(interaction: Interaction[Melody]) -> None:
    statistics = await database.query_statistics()

    return await interaction.response.send_message(embed=statistics_embed(statistics))
