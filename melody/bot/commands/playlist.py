from discord import Interaction

from melody.bot.core import Melody, client
from melody.bot.embeds import inaccessible_embed, not_found_embed, playlist_embed
from melody.bot.files import at_path
from melody.bot.transformers import UUIDTransform
from melody.kit.core import config, database
from melody.kit.predicates import playlist_predicate

NOT_FOUND = "Playlist with ID `{}` not found."
not_found = NOT_FOUND.format

INACCESSIBLE = "Playlist with ID `{}` is inaccessible."
inaccessible = INACCESSIBLE.format


@client.tree.command(name="playlist", description="Fetches playlists.")
async def get_playlist(interaction: Interaction[Melody], playlist_id: UUIDTransform) -> None:
    playlist = await database.query_playlist(playlist_id=playlist_id)

    if playlist is None:
        return await interaction.response.send_message(
            embed=not_found_embed(not_found(playlist_id))
        )

    discord_id = str(interaction.user.id)

    user = await database.query_user_by_discord_id(discord_id=discord_id)

    user_id_option = None if user is None else user.id

    predicate = playlist_predicate(user_id_option)

    if not await predicate(playlist):
        return await interaction.response.send_message(
            embed=inaccessible_embed(inaccessible(playlist_id))
        )

    result = at_path(config.images / playlist.uri.image_name)

    if result is None:
        return await interaction.response.send_message(embed=playlist_embed(playlist))

    file, url = result

    return await interaction.response.send_message(embed=playlist_embed(playlist, url), file=file)
