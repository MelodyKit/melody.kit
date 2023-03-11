from typing import List, Optional
from uuid import UUID

from attrs import define, field
from edgedb import AsyncIOClient, create_async_client  # type: ignore
from iters import iter

from melody.kit.constants import KIT_ROOT
from melody.kit.enums import PrivacyType
from melody.kit.models.album import Album, AlbumTracks, album_from_object
from melody.kit.models.artist import Artist, ArtistAlbums, ArtistTracks, artist_from_object
from melody.kit.models.base import Base, base_from_object
from melody.kit.models.playlist import (
    Playlist,
    PlaylistFollowers,
    PlaylistTracks,
    partial_playlist_from_object,
    playlist_from_object,
)
from melody.kit.models.statistics import Statistics, statistics_from_object
from melody.kit.models.track import (
    Track,
    partial_track_from_object,
    position_track_from_object,
    track_from_object,
)
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
from melody.kit.models.user_stream import user_stream_from_object
from melody.shared.constants import DEFAULT_ENCODING, DEFAULT_ERRORS
from melody.shared.typing import IntoPath

__all__ = ("Database",)

# NOTE: any is everywhere! we need to be cautious!

QUERIES_NAME = "queries"
QUERIES = KIT_ROOT / QUERIES_NAME

QUERY_SUFFIX = ".edgeql"


def load_query(
    path: IntoPath, encoding: str = DEFAULT_ENCODING, errors: str = DEFAULT_ERRORS
) -> str:
    return (QUERIES / path).with_suffix(QUERY_SUFFIX).read_text(encoding, errors)


# tracks

QUERY_TRACK = load_query("tracks/query")
DELETE_TRACK = load_query("tracks/delete")

# artists

QUERY_ARTIST = load_query("artists/query")
DELETE_ARTIST = load_query("artists/delete")

QUERY_ARTIST_TRACKS = load_query("artists/tracks/query")
QUERY_ARTIST_ALBUMS = load_query("artists/albums/query")

# albums

QUERY_ALBUM = load_query("albums/query")
DELETE_ALBUM = load_query("albums/delete")

QUERY_ALBUM_TRACKS = load_query("albums/tracks/query")

# playlists

INSERT_PLAYLIST = load_query("playlists/insert")
QUERY_PLAYLIST = load_query("playlists/query")
DELETE_PLAYLIST = load_query("playlists/delete")
CHECK_PLAYLIST = load_query("playlists/check")
UPDATE_PLAYLIST = load_query("playlists/update")

QUERY_PLAYLIST_FOLLOWERS = load_query("playlists/followers/query")

INSERT_PLAYLIST_FOLLOWER = load_query("playlists/followers/insert")
DELETE_PLAYLIST_FOLLOWER = load_query("playlists/followers/delete")

QUERY_PLAYLIST_TRACKS = load_query("playlists/tracks/query")

# users

QUERY_USER = load_query("users/query")

INSERT_USER = load_query("users/insert")
UPDATE_USER_PASSWORD_HASH = load_query("users/update_password_hash")
UPDATE_USER_VERIFIED = load_query("users/update_verified")
DELETE_USER = load_query("users/delete")

QUERY_USER_TRACKS = load_query("users/tracks/query")
SAVE_USER_TRACKS = load_query("users/tracks/save")
REMOVE_USER_TRACKS = load_query("users/tracks/remove")

QUERY_USER_ARTISTS = load_query("users/artists/query")
SAVE_USER_ARTISTS = load_query("users/artists/save")
REMOVE_USER_ARTISTS = load_query("users/artists/remove")

QUERY_USER_ALBUMS = load_query("users/albums/query")
SAVE_USER_ALBUMS = load_query("users/albums/save")
REMOVE_USER_ALBUMS = load_query("users/albums/remove")

QUERY_USER_PLAYLISTS = load_query("users/playlists/query")

QUERY_USER_STREAMS = load_query("users/streams/query")

QUERY_USER_FOLLOWERS = load_query("users/followers/query")
QUERY_USER_FOLLOWING = load_query("users/following/query")

QUERY_USER_FRIENDS = load_query("users/friends/query")
CHECK_USER_FRIENDS = load_query("users/friends/check")

QUERY_USER_INFO_BY_EMAIL = load_query("users/info/query_by_email")

# statistics

QUERY_STATISTICS = load_query("statistics/query")


@define()
class Database:
    client: AsyncIOClient = field(factory=create_async_client)

    async def query_track(self, track_id: UUID) -> Optional[Track]:
        option = await self.client.query_single(QUERY_TRACK, track_id=track_id)  # type: ignore

        return None if option is None else track_from_object(option)

    async def delete_track(self, track_id: UUID) -> None:
        await self.client.query_single(DELETE_TRACK, track_id=track_id)  # type: ignore

    async def query_artist(self, artist_id: UUID) -> Optional[Artist]:
        option = await self.client.query_single(QUERY_ARTIST, artist_id=artist_id)  # type: ignore

        return None if option is None else artist_from_object(option)

    async def query_artist_tracks(self, artist_id: UUID) -> Optional[ArtistTracks]:
        option = await self.client.query_single(  # type: ignore
            QUERY_ARTIST_TRACKS, artist_id=artist_id
        )

        return None if option is None else iter(option.tracks).map(track_from_object).list()

    async def query_artist_albums(self, artist_id: UUID) -> Optional[ArtistAlbums]:
        option = await self.client.query_single(  # type: ignore
            QUERY_ARTIST_ALBUMS, artist_id=artist_id
        )

        return None if option is None else iter(option.albums).map(album_from_object).list()

    async def delete_artist(self, artist_id: UUID) -> None:
        await self.client.query_single(DELETE_ARTIST, artist_id=artist_id)  # type: ignore

    async def query_album(self, album_id: UUID) -> Optional[Album]:
        option = await self.client.query_single(QUERY_ALBUM, album_id=album_id)  # type: ignore

        return None if option is None else album_from_object(option)

    async def query_album_tracks(self, album_id: UUID) -> Optional[AlbumTracks]:
        option = await self.client.query_single(  # type: ignore
            QUERY_ALBUM_TRACKS, album_id=album_id
        )

        return None if option is None else iter(option.tracks).map(partial_track_from_object).list()

    async def delete_album(self, album_id: UUID) -> None:
        await self.client.query_single(DELETE_ALBUM, album_id=album_id)  # type: ignore

    async def insert_playlist(
        self,
        name: str,
        description: str,
        privacy_type: PrivacyType,
        user_id: UUID,
    ) -> Base:
        object = await self.client.query_single(  # type: ignore
            INSERT_PLAYLIST,
            name=name,
            description=description,
            privacy_type=privacy_type.value,
            user_id=user_id,
        )

        return base_from_object(object)

    async def query_playlist(self, playlist_id: UUID) -> Optional[Playlist]:
        option = await self.client.query_single(  # type: ignore
            QUERY_PLAYLIST, playlist_id=playlist_id
        )

        return None if option is None else playlist_from_object(option)

    async def delete_playlist(self, playlist_id: UUID) -> None:
        await self.client.query_single(DELETE_PLAYLIST, playlist_id=playlist_id)  # type: ignore

    async def check_playlist(self, playlist_id: UUID, user_id: UUID) -> bool:
        option = await self.client.query_single(  # type: ignore
            CHECK_PLAYLIST, playlist_id=playlist_id, user_id=user_id
        )

        return option is not None

    async def update_playlist(
        self, playlist_id: UUID, name: str, description: str, privacy_type: PrivacyType
    ) -> None:
        await self.client.query_single(  # type: ignore
            UPDATE_PLAYLIST,
            playlist_id=playlist_id,
            name=name,
            description=description,
            privacy_type=privacy_type.value,
        )

    async def query_playlist_followers(self, playlist_id: UUID) -> Optional[PlaylistFollowers]:
        option = await self.client.query_single(QUERY_PLAYLIST_FOLLOWERS, playlist_id=playlist_id)

        return None if option is None else iter(option.followers).map(user_from_object).list()

    async def insert_playlist_follower(self, playlist_id: UUID, user_id: UUID) -> None:
        await self.client.query_single(
            INSERT_PLAYLIST_FOLLOWER, playlist_id=playlist_id, user_id=user_id
        )

    async def delete_playlist_follower(self, playlist_id: UUID, user_id: UUID) -> None:
        await self.client.query_single(
            DELETE_PLAYLIST_FOLLOWER, playlist_id=playlist_id, user_id=user_id
        )

    async def query_playlist_tracks(self, playlist_id: UUID) -> Optional[PlaylistTracks]:
        option = await self.client.query_single(  # type: ignore
            QUERY_PLAYLIST_TRACKS, playlist_id=playlist_id
        )

        return (
            None if option is None else iter(option.tracks).map(position_track_from_object).list()
        )

    async def query_user(self, user_id: UUID) -> Optional[User]:
        option = await self.client.query_single(QUERY_USER, user_id=user_id)  # type: ignore

        return None if option is None else user_from_object(option)

    async def insert_user(self, name: str, email: str, password_hash: str) -> Base:
        object = await self.client.query_single(  # type: ignore
            INSERT_USER, name=name, email=email, password_hash=password_hash
        )

        return base_from_object(object)

    async def update_user_password_hash(self, user_id: UUID, password_hash: str) -> None:
        await self.client.query_single(  # type: ignore
            UPDATE_USER_PASSWORD_HASH, user_id=user_id, password_hash=password_hash
        )

    async def update_user_verified(self, user_id: UUID, verified: bool) -> None:
        await self.client.query_single(  # type: ignore
            UPDATE_USER_VERIFIED, user_id=user_id, verified=verified
        )

    async def delete_user(self, user_id: UUID) -> None:
        await self.client.query_single(DELETE_USER, user_id=user_id)  # type: ignore

    async def query_user_tracks(self, user_id: UUID) -> Optional[UserTracks]:
        option = await self.client.query_single(QUERY_USER_TRACKS, user_id=user_id)  # type: ignore

        return None if option is None else iter(option.tracks).map(track_from_object).list()

    async def save_user_tracks(self, user_id: UUID, ids: List[UUID]) -> None:
        await self.client.query_single(SAVE_USER_TRACKS, user_id=user_id, ids=ids)  # type: ignore

    async def remove_user_tracks(self, user_id: UUID, ids: List[UUID]) -> None:
        await self.client.query_single(REMOVE_USER_TRACKS, user_id=user_id, ids=ids)  # type: ignore

    async def query_user_artists(self, user_id: UUID) -> Optional[UserArtists]:
        option = await self.client.query_single(QUERY_USER_ARTISTS, user_id=user_id)  # type: ignore

        return None if option is None else iter(option.artists).map(artist_from_object).list()

    async def save_user_artists(self, user_id: UUID, ids: List[UUID]) -> None:
        await self.client.query_single(SAVE_USER_ARTISTS, user_id=user_id, ids=ids)  # type: ignore

    async def remove_user_artists(self, user_id: UUID, ids: List[UUID]) -> None:
        await self.client.query_single(  # type: ignore
            REMOVE_USER_ARTISTS, user_id=user_id, ids=ids
        )

    async def query_user_albums(self, user_id: UUID) -> Optional[UserAlbums]:
        option = await self.client.query_single(QUERY_USER_ALBUMS, user_id=user_id)  # type: ignore

        return None if option is None else iter(option.albums).map(album_from_object).list()

    async def save_user_albums(self, user_id: UUID, ids: List[UUID]) -> None:
        await self.client.query_single(SAVE_USER_ALBUMS, user_id=user_id, ids=ids)  # type: ignore

    async def remove_user_albums(self, user_id: UUID, ids: List[UUID]) -> None:
        await self.client.query_single(REMOVE_USER_ALBUMS, user_id=user_id, ids=ids)  # type: ignore

    async def query_user_playlists(self, user_id: UUID) -> Optional[UserPlaylists]:
        option = await self.client.query_single(  # type: ignore
            QUERY_USER_PLAYLISTS, user_id=user_id
        )

        return (
            None
            if option is None
            else iter(option.playlists).map(partial_playlist_from_object).list()
        )

    async def query_user_streams(self, user_id: UUID) -> Optional[UserStreams]:
        option = await self.client.query_single(QUERY_USER_STREAMS, user_id=user_id)  # type: ignore

        return None if option is None else iter(option.streams).map(user_stream_from_object).list()

    async def query_user_followers(self, user_id: UUID) -> Optional[UserFollowers]:
        option = await self.client.query_single(  # type: ignore
            QUERY_USER_FOLLOWERS, user_id=user_id
        )

        return None if option is None else iter(option.followers).map(user_from_object).list()

    async def query_user_following(self, user_id: UUID) -> Optional[UserFollowing]:
        option = await self.client.query_single(  # type: ignore
            QUERY_USER_FOLLOWING, user_id=user_id
        )

        return None if option is None else iter(option.following).map(user_from_object).list()

    async def query_user_friends(self, user_id: UUID) -> Optional[UserFriends]:
        option = await self.client.query_single(QUERY_USER_FRIENDS, user_id=user_id)  # type: ignore

        return None if option is None else iter(option.friends).map(user_from_object).list()

    async def check_user_friends(self, user_id: UUID, target_id: UUID) -> bool:
        option = await self.client.query_single(  # type: ignore
            CHECK_USER_FRIENDS, user_id=user_id, target_id=target_id
        )

        return option is not None

    async def query_user_info_by_email(self, email: str) -> Optional[UserInfo]:
        option = await self.client.query_single(  # type: ignore
            QUERY_USER_INFO_BY_EMAIL, email=email
        )

        return None if option is None else user_info_from_object(option)

    async def query_statistics(self) -> Statistics:
        object = await self.client.query_required_single(QUERY_STATISTICS)  # type: ignore

        return statistics_from_object(object)
