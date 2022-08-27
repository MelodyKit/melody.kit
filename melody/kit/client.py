from attrs import define, field
from edgedb import AsyncIOClient, create_async_client  # type: ignore

__all__ = ("Client",)

TRACK = """
select Track {
    id,
    name,
    spotify_id,
    apple_music_id,
    yandex_music_id,
    artists: {
        id,
        name,
        spotify_id,
        apple_music_id,
        yandex_music_id,
    },
    albums: {
        id,
        name,
        spotify_id,
        apple_music_id,
        yandex_music_id,
    }
} filter .id = <uuid>$id;
"""


@define()
class Client:
    database: AsyncIOClient = field(factory=create_async_client)
