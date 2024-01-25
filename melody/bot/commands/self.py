from discord import Interaction

from melody.bot.core import Melody, client
from melody.bot.embeds import not_linked_embed, user_embed
from melody.bot.files import at_path
from melody.kit.core import config, database

NOT_LINKED = "User with ID `{}` is not linked to MelodyKit."
not_linked = NOT_LINKED.format


@client.tree.command(name="self", description="Fetches self users.")
async def get_self(interaction: Interaction[Melody]) -> None:
    discord_id = str(interaction.user.id)

    self = await database.query_user_by_discord_id(discord_id=discord_id)

    if self is None:
        return await interaction.response.send_message(
            embed=not_linked_embed(not_linked(discord_id))
        )

    result = at_path(config.images / self.uri.image_name)

    if result is None:
        return await interaction.response.send_message(embed=user_embed(self))

    file, url = result

    return await interaction.response.send_message(embed=user_embed(self, url), file=file)
