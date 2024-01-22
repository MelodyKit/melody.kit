from typing import Optional

from discord import Embed, File, Interaction

from melody.bot.colors import color_into_discord, random_melody_color
from melody.bot.constants import INLINE
from melody.bot.core import Melody, client
from melody.bot.errors import not_found_embed
from melody.bot.transformers import UUIDTransform
from melody.bot.utils import count, links, tick
from melody.kit.core import config, database
from melody.kit.models.user import User

__all__ = ("get_user",)

NOT_FOUND = "User with ID `{}` not found."
not_found = NOT_FOUND.format

PRIVACY_TYPE = "Privacy Type"
FOLLOWERS = "Followers"
STREAMS = "Streams"
LINKS = "Links"

ATTACHMENT = "attachment://{}"
attachment = ATTACHMENT.format


def user_embed(user: User, image_name: Optional[str] = None, inline: bool = INLINE) -> Embed:
    embed = (
        Embed(color=color_into_discord(random_melody_color()), title=user.name, url=user.url)
        .add_field(name=PRIVACY_TYPE, value=tick(user.privacy_type.value), inline=inline)
        .add_field(name=FOLLOWERS, value=count(user.follower_count), inline=inline)
        .add_field(name=STREAMS, value=count(user.stream_count), inline=inline)
        .add_field(name=LINKS, value=links(user), inline=inline)
    )

    if image_name is None:
        return embed

    return embed.set_image(url=attachment(image_name))


@client.tree.command(name="user", description="Fetches users.")
async def get_user(interaction: Interaction[Melody], user_id: UUIDTransform) -> None:
    user = await database.query_user(user_id=user_id)

    if user is None:
        return await interaction.response.send_message(embed=not_found_embed(not_found(user_id)))

    path = config.images / user.uri.image_name

    if not path.exists():
        return await interaction.response.send_message(embed=user_embed(user))

    name = path.name

    image = File(path, name)

    return await interaction.response.send_message(embed=user_embed(user, name), file=image)
