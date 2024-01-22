from discord import Embed, Interaction
from iters.iters import iter

from melody.bot.colors import color_into_discord, random_melody_color
from melody.bot.constants import INLINE, SEPARATOR
from melody.bot.core import Melody, client
from melody.bot.errors import not_found_embed
from melody.bot.transformers import UUIDTransform
from melody.bot.utils import artist_with_url, count, duration_ms, links, tick
from melody.kit.core import database
from melody.kit.models.album import Album

__all__ = ("get_album",)

NOT_FOUND = "Album with ID `{}` not found."
not_found = NOT_FOUND.format


ARTISTS = "Artists"
TYPE = "Type"
DURATION = "Duration"
TRACKS = "Tracks"
RELEASE_DATE = "Release Date"
LABEL = "Label"
LINKS = "Links"


def album_embed(album: Album, inline: bool = INLINE) -> Embed:
    return (
        Embed(color=color_into_discord(random_melody_color()), title=album.name, url=album.url)
        .add_field(
            name=ARTISTS,
            value=iter(album.artists).map(artist_with_url).join(SEPARATOR),
            inline=inline,
        )
        .add_field(name=TYPE, value=tick(album.album_type.value), inline=inline)
        .add_field(name=TRACKS, value=count(album.track_count), inline=inline)
        .add_field(name=DURATION, value=tick(duration_ms(album.duration_ms)), inline=inline)
        .add_field(name=RELEASE_DATE, value=tick(album.release_date), inline=inline)
        .add_field(name=LABEL, value=album.label, inline=inline)
        .add_field(name=LINKS, value=links(album), inline=inline)
    )


@client.tree.command(name="album", description="Fetches albums.")
async def get_album(interaction: Interaction[Melody], album_id: UUIDTransform) -> None:
    album = await database.query_album(album_id=album_id)

    if album is None:
        return await interaction.response.send_message(embed=not_found_embed(not_found(album_id)))

    return await interaction.response.send_message(embed=album_embed(album))
