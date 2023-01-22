from pathlib import Path
from typing import Optional
from uuid import UUID

from attrs import define, field
from edgedb import AsyncIOClient, create_async_client  # type: ignore
from iters import iter

from melody.kit.models import (
    Abstract,
    Album,
    AlbumTracks,
    Artist,
    Playlist,
    PlaylistTracks,
    Track,
    User,
    UserInfo,
    abstract_from_object,
    album_from_object,
    artist_from_object,
    playlist_from_object,
    track_from_object,
    user_from_object,
    user_info_from_object,
)

__all__ = ("Database",)

# NOTE: any is everywhere! we need to be cautious!

QUERIES_NAME = "queries"
QUERIES = Path(__file__).parent / QUERIES_NAME

QUERY = "{}.edgeql"
query = QUERY.format


def load_query(name: str) -> str:
    with open(QUERIES / query(name)) as file:
        return file.read().strip()


CHECK_FRIENDS = load_query("check_friends")

TRACK = load_query("track")

ARTIST = load_query("artist")

ALBUM = load_query("album")
ALBUM_TRACKS = load_query("album_tracks")

PLAYLIST = load_query("playlist")
PLAYLIST_TRACKS = load_query("playlist_tracks")

USER = load_query("user")

INSERT_USER = load_query("insert_user")
UPDATE_USER_PASSWORD_HASH = load_query("update_user_password_hash")

USER_INFO_BY_EMAIL = load_query("user_info_by_email")


@define()
class Database:
    client: AsyncIOClient = field(factory=create_async_client)

    async def check_friends(self, user_id: UUID, target_id: UUID) -> bool:
        option = await self.client.query_single(  # type: ignore
            CHECK_FRIENDS, user_id=user_id, target_id=target_id
        )

        return option is not None

    async def query_track(self, track_id: UUID) -> Optional[Track]:
        option = await self.client.query_single(TRACK, track_id=track_id)  # type: ignore

        return None if option is None else track_from_object(option)

    async def query_artist(self, artist_id: UUID) -> Optional[Artist]:
        option = await self.client.query_single(ARTIST, artist_id=artist_id)  # type: ignore

        return None if option is None else artist_from_object(option)

    async def query_album(self, album_id: UUID) -> Optional[Album]:
        option = await self.client.query_single(ALBUM, album_id=album_id)  # type: ignore

        return None if option is None else album_from_object(option)

    async def query_album_tracks(self, album_id: UUID) -> Optional[AlbumTracks]:
        option = await self.client.query_single(ALBUM_TRACKS, album_id=album_id)  # type: ignore

        return None if option is None else iter(option.tracks).map(track_from_object).list()

    async def query_playlist(self, playlist_id: UUID) -> Optional[Playlist]:
        option = await self.client.query_single(PLAYLIST, playlist_id=playlist_id)  # type: ignore

        return None if option is None else playlist_from_object(option)

    async def query_playlist_tracks(self, playlist_id: UUID) -> Optional[PlaylistTracks]:
        option = await self.client.query_single(PLAYLIST_TRACKS, playlist_id=playlist_id)  # type: ignore

        return None if option is None else iter(option.tracks).map(track_from_object).list()

    async def query_user(self, user_id: UUID) -> Optional[User]:
        option = await self.client.query_single(USER, user_id=user_id)  # type: ignore

        return None if option is None else user_from_object(option)

    async def insert_user(self, name: str, email: str, password_hash: str) -> Abstract:
        object = await self.client.query_single(  # type: ignore
            INSERT_USER, name=name, email=email, password_hash=password_hash
        )

        return abstract_from_object(object)

    async def update_user_password_hash(self, user_id: UUID, password_hash: str) -> None:
        await self.client.query_single(  # type: ignore
            UPDATE_USER_PASSWORD_HASH, user_id=user_id, password_hash=password_hash
        )

    async def query_user_info_by_email(self, email: str) -> Optional[UserInfo]:
        option = await self.client.query_single(USER_INFO_BY_EMAIL, email=email)  # type: ignore

        return None if option is None else user_info_from_object(option)
