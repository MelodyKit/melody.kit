from discord import Interaction

from melody.bot.core import Melody, client
from melody.bot.embeds import statistics_embed
from melody.kit.core import database

__all__ = ("get_statistics",)


@client.tree.command(name="statistics", description="Fetches overall statistics.")
async def get_statistics(interaction: Interaction[Melody]) -> None:
    statistics = await database.query_statistics()

    return await interaction.response.send_message(embed=statistics_embed(statistics))
