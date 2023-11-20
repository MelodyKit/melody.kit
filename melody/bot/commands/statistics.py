from random import choice

from discord import Color, Embed, Interaction

from melody.bot.constants import INLINE
from melody.bot.core import Melody, client
from melody.kit.core import database
from melody.shared.constants import MELODY_COLORS

COUNT = "{:,}"
count = COUNT.format

STATISTICS = "Statistics"
USERS = "Users"
STREAMS = "Streams"
TRACKS = "Tracks"
ARTISTS = "Artists"
ALBUMS = "Albums"
PLAYLISTS = "Playlists"


@client.tree.command(name="statistics", description="Fetches overall statistics.")
async def get_statistics(interaction: Interaction[Melody]) -> None:
    statistics = await database.query_statistics()

    embed = (
        Embed(color=Color(choice(MELODY_COLORS).value), title=STATISTICS)
        .add_field(name=USERS, value=count(statistics.user_count), inline=INLINE)
        .add_field(name=STREAMS, value=count(statistics.stream_count), inline=INLINE)
        .add_field(name=TRACKS, value=count(statistics.track_count), inline=INLINE)
        .add_field(name=ARTISTS, value=count(statistics.artist_count), inline=INLINE)
        .add_field(name=ALBUMS, value=count(statistics.album_count), inline=INLINE)
        .add_field(name=PLAYLISTS, value=count(statistics.playlist_count), inline=INLINE)
    )

    await interaction.response.send_message(embed=embed)
