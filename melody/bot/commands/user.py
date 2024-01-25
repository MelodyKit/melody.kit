from discord import Interaction

from melody.bot.core import Melody, client
from melody.bot.embeds import not_found_embed, user_embed
from melody.bot.files import at_path
from melody.bot.transformers import UUIDTransform
from melody.kit.core import config, database

__all__ = ("get_user",)

NOT_FOUND = "User with ID `{}` not found."
not_found = NOT_FOUND.format


@client.tree.command(name="user", description="Fetches users.")
async def get_user(interaction: Interaction[Melody], user_id: UUIDTransform) -> None:
    user = await database.query_user(user_id=user_id)

    if user is None:
        return await interaction.response.send_message(embed=not_found_embed(not_found(user_id)))

    result = at_path(config.images / user.uri.image_name)

    if result is None:
        return await interaction.response.send_message(embed=user_embed(user))

    file, url = result

    return await interaction.response.send_message(embed=user_embed(user, url), file=file)
