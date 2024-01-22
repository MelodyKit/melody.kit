from discord import Interaction

from melody.bot.core import Melody, client

__all__ = ("search_items",)


@client.tree.command(name="search", description="Searches for items.")
async def search_items(interaction: Interaction[Melody], query: str) -> None:
    pass
