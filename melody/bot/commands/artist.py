from discord import Interaction

from melody.bot.core import Melody, client
from melody.bot.embeds import artist_embed, not_found_embed
from melody.bot.transformers import UUIDTransform
from melody.kit.core import database

__all__ = ("get_artist",)

NOT_FOUND = "Artist with ID `{}` not found."
not_found = NOT_FOUND.format


@client.tree.command(name="artist", description="Fetches artists.")
async def get_artist(interaction: Interaction[Melody], artist_id: UUIDTransform) -> None:
    artist = await database.query_artist(artist_id=artist_id)

    if artist is None:
        return await interaction.response.send_message(embed=not_found_embed(not_found(artist_id)))

    return await interaction.response.send_message(embed=artist_embed(artist))
