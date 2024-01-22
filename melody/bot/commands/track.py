from discord import Embed, Interaction
from iters.iters import iter

from melody.bot.colors import color_into_discord, random_melody_color
from melody.bot.constants import INLINE, SEPARATOR
from melody.bot.core import Melody, client
from melody.bot.errors import not_found_embed
from melody.bot.transformers import UUIDTransform
from melody.bot.utils import album_with_url, artist_with_url, count, duration_ms, links, tick
from melody.kit.core import database
from melody.kit.models.tracks import Track

__all__ = ("get_track",)

NOT_FOUND = "Track with ID `{}` not found."
not_found = NOT_FOUND.format


ARTISTS = "Artists"
ALBUM = "Album"
LINKS = "Links"
DURATION = "Duration"
STREAMS = "Streams"


def track_embed(track: Track, inline: bool = INLINE) -> Embed:
    return (
        Embed(color=color_into_discord(random_melody_color()), title=track.name, url=track.url)
        .add_field(
            name=ARTISTS,
            value=iter(track.artists).map(artist_with_url).join(SEPARATOR),
            inline=inline,
        )
        .add_field(name=ALBUM, value=album_with_url(track.album), inline=inline)
        .add_field(name=DURATION, value=tick(duration_ms(track.duration_ms)), inline=inline)
        .add_field(name=STREAMS, value=count(track.stream_count), inline=inline)
        .add_field(name=LINKS, value=links(track), inline=inline)
    )


@client.tree.command(name="track", description="Fetches tracks.")
async def get_track(interaction: Interaction[Melody], track_id: UUIDTransform) -> None:
    track = await database.query_track(track_id=track_id)

    if track is None:
        return await interaction.response.send_message(embed=not_found_embed(not_found(track_id)))

    return await interaction.response.send_message(embed=track_embed(track))
