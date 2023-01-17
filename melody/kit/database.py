from uuid import UUID

from attrs import define, field
from edgedb import AsyncIOClient, create_async_client  # type: ignore

from melody.kit.models import Album, Track

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

ALBUM = """
select Album {
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
    tracks: {
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
        explicit,
        created_at,
        spotify_id,
        apple_music_id,
        yandex_music_id
    },
    album_type,
    release_date,
    label,
    track_count,
    created_at,
    spotify_id,
    apple_music_id,
    yandex_music_id
} filter .id = <uuid>$id;
"""


@define()
class Database:
    client: AsyncIOClient = field(factory=create_async_client)

    async def query_track(self, track_id: UUID) -> Track:
        object = await self.client.query_required_single(TRACK, id=track_id)  # type: ignore

        return Track.from_object(object)

    async def query_album(self, album_id: UUID) -> Album:
        object = await self.client.query_required_single(ALBUM, id=album_id)  # type: ignore

        return Album.from_object(object)
