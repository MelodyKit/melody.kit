from random import choice

from discord import Color, Embed, Interaction

from melody.bot.constants import INLINE
from melody.bot.core import client
from melody.kit.core import database
from melody.shared.constants import MELODY_COLORS

COUNT = "{:,}"
count = COUNT.format


@client.tree.command(name="statistics", description="Fetches overall statistics.")
async def get_statistics(interaction: Interaction) -> None:
    statistics = await database.query_statistics()

    embed = (
        Embed(color=Color(choice(MELODY_COLORS)), title="Statistics")
        .add_field(name="Users", value=count(statistics.user_count), inline=INLINE)
        .add_field(name="Streams", value=count(statistics.stream_count), inline=INLINE)
        .add_field(name="Tracks", value=count(statistics.track_count), inline=INLINE)
        .add_field(name="Artists", value=count(statistics.artist_count), inline=INLINE)
        .add_field(name="Albums", value=count(statistics.album_count), inline=INLINE)
        .add_field(name="Playlists", value=count(statistics.playlist_count), inline=INLINE)
    )

    await interaction.response.send_message(embed=embed)
