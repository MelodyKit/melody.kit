from discord import Interaction

from melody.bot.core import Melody, client
from melody.bot.embeds import inaccessible_embed, not_found_embed, playlist_embed
from melody.bot.files import at_path
from melody.bot.transformers import UUIDTransform
from melody.kit.core import config, database
from melody.kit.privacy import are_friends, is_playlist_accessible, is_playlist_public

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

    self = await database.query_user_by_discord_id(discord_id=discord_id)

    if self is None:
        accessible = is_playlist_public(playlist)

    else:
        self_id = self.id

        playlist_user = playlist.user

        friends = await are_friends(self_id, playlist_user.id)

        accessible = is_playlist_accessible(self_id, playlist, playlist_user, friends)

    if not accessible:
        return await interaction.response.send_message(
            embed=inaccessible_embed(inaccessible(playlist_id))
        )

    result = at_path(config.images / playlist.uri.image_name)

    if result is None:
        return await interaction.response.send_message(embed=playlist_embed(playlist))

    file, url = result

    return await interaction.response.send_message(embed=playlist_embed(playlist, url), file=file)
