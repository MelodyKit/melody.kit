from typing import Optional
from uuid import UUID

from attrs import define, field
from edgedb import AsyncIOClient, create_async_client  # type: ignore
from iters import iter

from melody.kit.constants import KIT_ROOT
from melody.kit.models.abstract import Abstract, abstract_from_object
from melody.kit.models.album import Album, AlbumTracks, album_from_object
from melody.kit.models.artist import Artist, ArtistAlbums, ArtistTracks, artist_from_object
from melody.kit.models.playlist import Playlist, PlaylistTracks, playlist_from_object
from melody.kit.models.statistics import Statistics, statistics_from_object
from melody.kit.models.track import Track, track_from_object
from melody.kit.models.user import (
    User,
    UserAlbums,
    UserArtists,
    UserFollowers,
    UserFollowing,
    UserFriends,
    UserPlaylists,
    UserStreams,
    UserTracks,
    user_from_object,
)
from melody.kit.models.user_info import UserInfo, user_info_from_object

__all__ = ("Database",)

# NOTE: any is everywhere! we need to be cautious!

QUERIES_NAME = "queries"
QUERIES = KIT_ROOT / QUERIES_NAME

QUERY = "{}.edgeql"
query = QUERY.format


def load_query(name: str) -> str:
    with open(QUERIES / query(name)) as file:
        return file.read().strip()


CHECK_FRIENDS = load_query("check_friends")

TRACK = load_query("track")

ARTIST = load_query("artist")
ARTIST_TRACKS = load_query("artist_tracks")
ARTIST_ALBUMS = load_query("artist_albums")

ALBUM = load_query("album")
ALBUM_TRACKS = load_query("album_tracks")

PLAYLIST = load_query("playlist")
PLAYLIST_TRACKS = load_query("playlist_tracks")

USER = load_query("user")
USER_TRACKS = load_query("user_tracks")
USER_ARTISTS = load_query("user_artists")
USER_ALBUMS = load_query("user_albums")
USER_PLAYLISTS = load_query("user_playlists")

USER_STREAMS = load_query("user_streams")

USER_FRIENDS = load_query("user_friends")
USER_FOLLOWERS = load_query("user_followers")
USER_FOLLOWING = load_query("user_following")

INSERT_USER = load_query("insert_user")
UPDATE_USER_PASSWORD_HASH = load_query("update_user_password_hash")
UPDATE_USER_VERIFIED = load_query("update_user_verified")

USER_INFO_BY_EMAIL = load_query("user_info_by_email")

STATISTICS = load_query("statistics")


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

    async def query_artist_tracks(self, artist_id: UUID) -> Optional[ArtistTracks]:
        option = await self.client.query_single(ARTIST_TRACKS, artist_id=artist_id)  # type: ignore

        return None if option is None else iter(option.tracks).map(track_from_object).list()

    async def query_artist_albums(self, artist_id: UUID) -> Optional[ArtistAlbums]:
        option = await self.client.query_single(ARTIST_ALBUMS, artist_id=artist_id)  # type: ignore

        return None if option is None else iter(option.albums).map(album_from_object).list()

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

    async def query_user_tracks(self, user_id: UUID) -> Optional[UserTracks]:
        option = await self.client.query_single(USER_TRACKS, user_id=user_id)  # type: ignore

        return None if option is None else iter(option.tracks).map(track_from_object).list()

    async def query_user_artists(self, user_id: UUID) -> Optional[UserArtists]:
        option = await self.client.query_single(USER_ARTISTS, user_id=user_id)  # type: ignore

        return None if option is None else iter(option.artists).map(artist_from_object).list()

    async def query_user_albums(self, user_id: UUID) -> Optional[UserAlbums]:
        option = await self.client.query_single(USER_ALBUMS, user_id=user_id)  # type: ignore

        return None if option is None else iter(option.albums).map(album_from_object).list()

    async def query_user_playlists(self, user_id: UUID) -> Optional[UserPlaylists]:
        option = await self.client.query_single(USER_PLAYLISTS, user_id=user_id)  # type: ignore

        return None if option is None else iter(option.playlists).map(playlist_from_object).list()

    async def query_user_streams(self, user_id: UUID) -> Optional[UserStreams]:
        option = await self.client.query_single(USER_STREAMS, user_id=user_id)  # type: ignore

        return None if option is None else iter(option.streams).map(track_from_object).list()

    async def query_user_friends(self, user_id: UUID) -> Optional[UserFriends]:
        option = await self.client.query_single(USER_FRIENDS, user_id=user_id)  # type: ignore

        return None if option is None else iter(option.friends).map(user_from_object).list()

    async def query_user_followers(self, user_id: UUID) -> Optional[UserFollowers]:
        option = await self.client.query_single(USER_FOLLOWERS, user_id=user_id)  # type: ignore

        return None if option is None else iter(option.followers).map(user_from_object).list()

    async def query_user_following(self, user_id: UUID) -> Optional[UserFollowing]:
        option = await self.client.query_single(USER_FOLLOWING, user_id=user_id)  # type: ignore

        return None if option is None else iter(option.following).map(user_from_object).list()

    async def insert_user(self, name: str, email: str, password_hash: str) -> Abstract:
        object = await self.client.query_single(  # type: ignore
            INSERT_USER, name=name, email=email, password_hash=password_hash
        )

        return abstract_from_object(object)

    async def update_user_password_hash(self, user_id: UUID, password_hash: str) -> None:
        await self.client.query_single(  # type: ignore
            UPDATE_USER_PASSWORD_HASH, user_id=user_id, password_hash=password_hash
        )

    async def update_user_verified(self, user_id: UUID, verified: bool) -> None:
        await self.client.query_single(  # type: ignore
            UPDATE_USER_VERIFIED, user_id=user_id, verified=verified
        )

    async def query_user_info_by_email(self, email: str) -> Optional[UserInfo]:
        option = await self.client.query_single(USER_INFO_BY_EMAIL, email=email)  # type: ignore

        return None if option is None else user_info_from_object(option)

    async def query_statistics(self) -> Statistics:
        object = await self.client.query_required_single(STATISTICS)  # type: ignore

        return statistics_from_object(object)
