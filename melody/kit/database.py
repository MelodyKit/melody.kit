from uuid import UUID

from attrs import define, field
from edgedb import AsyncIOClient, create_async_client  # type: ignore

from melody.kit.models import Track

__all__ = ("Database",)

TRACK = """
select Track {
    id,
    name,
    artists: {
        id,
        name,
        created_at,
        spotify_id,
        apple_music_id,
        yandex_music_id
    },
    album: {
        id,
        name,
        album_type,
        release_date,
        track_count,
        created_at,
        spotify_id,
        apple_music_id,
        yandex_music_id
    },
    explicit,
    genres,
    created_at,
    spotify_id,
    apple_music_id,
    yandex_music_id
} filter .id = <uuid>$id;
"""


@define()
class Database:
    client: AsyncIOClient = field(factory=create_async_client)

    async def query_track(self, id: UUID) -> Track:
        object = await self.client.query_required_single(TRACK, id=id)  # type: ignore

        return Track.from_object(object)
