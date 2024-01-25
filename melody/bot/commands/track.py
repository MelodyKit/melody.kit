from discord import Interaction

from melody.bot.core import Melody, client
from melody.bot.embeds import not_found_embed, track_embed
from melody.bot.transformers import UUIDTransform
from melody.kit.core import database

__all__ = ("get_track",)

NOT_FOUND = "Track with ID `{}` not found."
not_found = NOT_FOUND.format


@client.tree.command(name="track", description="Fetches tracks.")
async def get_track(interaction: Interaction[Melody], track_id: UUIDTransform) -> None:
    track = await database.query_track(track_id=track_id)

    if track is None:
        return await interaction.response.send_message(embed=not_found_embed(not_found(track_id)))

    return await interaction.response.send_message(embed=track_embed(track))
