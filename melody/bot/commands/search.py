from discord import Interaction

from melody.bot.core import Melody, client
from melody.kit.enums import EntityType

__all__ = ("search_items",)


@client.tree.command(name="search", description="Searches for items.")
async def search_items(interaction: Interaction[Melody], type: EntityType, query: str) -> None:
    pass
