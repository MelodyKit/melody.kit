from discord import Interaction

from melody.bot.core import Melody, client
from melody.bot.embeds import album_embed, not_found_embed
from melody.bot.transformers import UUIDTransform
from melody.kit.core import database

__all__ = ("get_album",)

NOT_FOUND = "Album with ID `{}` not found."
not_found = NOT_FOUND.format


@client.tree.command(name="album", description="Fetches albums.")
async def get_album(interaction: Interaction[Melody], album_id: UUIDTransform) -> None:
    album = await database.query_album(album_id=album_id)

    if album is None:
        return await interaction.response.send_message(embed=not_found_embed(not_found(album_id)))

    return await interaction.response.send_message(embed=album_embed(album))
