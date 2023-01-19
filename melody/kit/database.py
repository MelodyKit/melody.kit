from uuid import UUID

from attrs import define, field
from edgedb import AsyncIOClient, create_async_client  # type: ignore

from melody.kit.models import Abstract, Album, Track, User, UserInfo

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

USER_INFO = """
select User {
    id,
    email,
    password_hash
} filter .email = <str>$email;
"""

INSERT_USER = """
insert User {
    name := <str>$name,
    email := <str>$email,
    password_hash := <str>$password_hash,
};
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

    async def query_user(self, user_id: UUID) -> User:
        ...

    async def query_user_info_by(self, email: str) -> UserInfo:
        object = await self.client.query_required_single(USER_INFO, email=email)  # type: ignore

        return UserInfo.from_object(object)

    async def insert_user(self, name: str, email: str, password_hash: str) -> Abstract:
        object = await self.client.query_required_single(  # type: ignore
            INSERT_USER, name=name, email=email, password_hash=password_hash
        )

        return Abstract.from_object(object)
