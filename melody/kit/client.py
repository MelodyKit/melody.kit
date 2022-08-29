from uuid import UUID

from attrs import define, field
from edgedb import AsyncIOClient, create_async_client  # type: ignore

from melody.kit.models import Track

__all__ = ("Client",)

TRACK = """
select Track {
    id,
    name,
    spotify_id,
    apple_music_id,
    yandex_music_id,
    genres,
    artists: {
        id,
        name,
        spotify_id,
        apple_music_id,
        yandex_music_id
    },
    albums: {
        id,
        name,
        spotify_id,
        apple_music_id,
        yandex_music_id,
        album_type,
        release_date,
        track_count
    }
} filter .id = <uuid>$id;
"""


@define()
class Client:
    database: AsyncIOClient = field(factory=create_async_client)

    async def query_track(self, id: UUID) -> Track:
        return Track.from_object(
            await self.database.query_required_single(TRACK, id=id)
        )
