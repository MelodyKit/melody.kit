from typing import List, Optional, Set, Tuple, TypeVar
from uuid import UUID

from attrs import define, field
from edgedb import AsyncIOClient, create_async_client
from iters.iters import iter
from typing_aliases import IntoPath

from melody.kit.constants import DEFAULT_LIMIT, DEFAULT_OFFSET, KIT_ROOT
from melody.kit.enums import Platform, PrivacyType
from melody.kit.models.album import Album
from melody.kit.models.artist import Artist
from melody.kit.models.base import Base
from melody.kit.models.client import Client
from melody.kit.models.client_info import ClientInfo
from melody.kit.models.playlist import Playlist
from melody.kit.models.privacy import PlaylistPrivacy, UserPrivacy
from melody.kit.models.statistics import Statistics
from melody.kit.models.streams import Stream
from melody.kit.models.tracks import PositionTrack, Track
from melody.kit.models.user import User
from melody.kit.models.user_info import UserInfo
from melody.kit.models.user_settings import UserSettings
from melody.shared.constants import DEFAULT_ENCODING, DEFAULT_ERRORS

__all__ = ("Database",)

T = TypeVar("T")

Counted = Tuple[List[T], int]

# NOTE: `Any` is everywhere! we need to be cautious!

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

SEARCH_TRACKS = load_query("tracks/search")

# artists

QUERY_ARTIST = load_query("artists/query")
DELETE_ARTIST = load_query("artists/delete")

SEARCH_ARTISTS = load_query("artists/search")

QUERY_ARTIST_TRACKS = load_query("artists/tracks/query")
QUERY_ARTIST_ALBUMS = load_query("artists/albums/query")

# albums

QUERY_ALBUM = load_query("albums/query")
DELETE_ALBUM = load_query("albums/delete")

SEARCH_ALBUMS = load_query("albums/search")

QUERY_ALBUM_TRACKS = load_query("albums/tracks/query")

# playlists

INSERT_PLAYLIST = load_query("playlists/insert")
QUERY_PLAYLIST = load_query("playlists/query")
DELETE_PLAYLIST = load_query("playlists/delete")
UPDATE_PLAYLIST = load_query("playlists/update")

SEARCH_PLAYLISTS = load_query("playlists/search")

QUERY_PLAYLIST_PRIVACY = load_query("playlists/query_privacy")

QUERY_PLAYLIST_TRACKS = load_query("playlists/tracks/query")

# users

QUERY_USER = load_query("users/query")

INSERT_USER = load_query("users/insert")
UPDATE_USER_PASSWORD_HASH = load_query("users/update_password_hash")
UPDATE_USER_VERIFIED = load_query("users/update_verified")
DELETE_USER = load_query("users/delete")

UPDATE_USER_SECRET = load_query("users/update_secret")

SEARCH_USERS = load_query("users/search")

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
ADD_USER_FOLLOWING = load_query("users/following/add")
REMOVE_USER_FOLLOWING = load_query("users/following/remove")

QUERY_USER_FOLLOWED_PLAYLISTS = load_query("users/playlists/followed/query")
ADD_USER_FOLLOWED_PLAYLISTS = load_query("users/playlists/followed/add")
REMOVE_USER_FOLLOWED_PLAYLISTS = load_query("users/playlists/followed/remove")

QUERY_USER_FRIENDS = load_query("users/friends/query")
QUERY_USER_FRIENDS_ESSENTIAL = load_query("users/friends/query_essential")
CHECK_USER_FRIENDS = load_query("users/friends/check")

QUERY_USER_PRIVACY = load_query("users/query_privacy")

QUERY_USER_INFO = load_query("users/query_info")
QUERY_USER_INFO_BY_EMAIL = load_query("users/query_info_by_email")

QUERY_USER_SETTINGS = load_query("users/settings/query")
UPDATE_USER_SETTINGS = load_query("users/settings/update")

UPDATE_USER_DISCORD_ID = load_query("users/connections/update_discord_id")
QUERY_USER_BY_DISCORD_ID = load_query("users/connections/query_by_discord_id")

# statistics

QUERY_STATISTICS = load_query("statistics/query")

# clients

QUERY_CLIENT = load_query("clients/query")
INSERT_CLIENT = load_query("clients/insert")
DELETE_CLIENT = load_query("clients/delete")
UPDATE_CLIENT = load_query("clients/update")

UPDATE_CLIENT_SECRET_HASH = load_query("clients/update_secret_hash")

QUERY_CLIENT_INFO = load_query("clients/query_info")


@define()
class Database:
    client: AsyncIOClient = field(factory=create_async_client)

    async def query_track(self, track_id: UUID) -> Optional[Track]:
        option = await self.client.query_single(QUERY_TRACK, track_id=track_id)

        return None if option is None else Track.from_object(option)

    async def delete_track(self, track_id: UUID) -> None:
        await self.client.query_single(DELETE_TRACK, track_id=track_id)

    async def search_tracks(
        self, query: str, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT
    ) -> List[Track]:
        result = await self.client.query(SEARCH_TRACKS, fts_query=query, offset=offset, limit=limit)

        return iter(result).map(Track.from_object).list()

    async def query_artist(self, artist_id: UUID) -> Optional[Artist]:
        option = await self.client.query_single(QUERY_ARTIST, artist_id=artist_id)

        return None if option is None else Artist.from_object(option)

    async def query_artist_tracks(
        self, artist_id: UUID, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT
    ) -> Optional[Counted[Track]]:
        option = await self.client.query_single(
            QUERY_ARTIST_TRACKS, artist_id=artist_id, offset=offset, limit=limit
        )

        return (
            None
            if option is None
            else (iter(option.tracks).map(Track.from_object).list(), option.track_count)
        )

    async def query_artist_albums(
        self, artist_id: UUID, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT
    ) -> Optional[Counted[Album]]:
        option = await self.client.query_single(
            QUERY_ARTIST_ALBUMS, artist_id=artist_id, offset=offset, limit=limit
        )

        return (
            None
            if option is None
            else (iter(option.albums).map(Album.from_object).list(), option.album_count)
        )

    async def delete_artist(self, artist_id: UUID) -> None:
        await self.client.query_single(DELETE_ARTIST, artist_id=artist_id)

    async def search_artists(
        self, query: str, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT
    ) -> List[Artist]:
        result = await self.client.query(
            SEARCH_ARTISTS, fts_query=query, offset=offset, limit=limit
        )

        return iter(result).map(Artist.from_object).list()

    async def query_album(self, album_id: UUID) -> Optional[Album]:
        option = await self.client.query_single(QUERY_ALBUM, album_id=album_id)

        return None if option is None else Album.from_object(option)

    async def query_album_tracks(
        self, album_id: UUID, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT
    ) -> Optional[Counted[Track]]:
        option = await self.client.query_single(
            QUERY_ALBUM_TRACKS, album_id=album_id, offset=offset, limit=limit
        )

        return (
            None
            if option is None
            else (
                iter(option.tracks).map(Track.from_object).list(),
                option.track_count,
            )
        )

    async def delete_album(self, album_id: UUID) -> None:
        await self.client.query_single(DELETE_ALBUM, album_id=album_id)

    async def search_albums(
        self, query: str, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT
    ) -> List[Album]:
        result = await self.client.query(SEARCH_ALBUMS, fts_query=query, offset=offset, limit=limit)

        return iter(result).map(Album.from_object).list()

    async def insert_playlist(
        self,
        name: str,
        description: Optional[str],
        privacy_type: PrivacyType,
        owner_id: UUID,
    ) -> Base:
        object = await self.client.query_single(
            INSERT_PLAYLIST,
            name=name,
            description=description,
            privacy_type=privacy_type.value,
            owner_id=owner_id,
        )

        return Base.from_object(object)

    async def query_playlist(self, playlist_id: UUID) -> Optional[Playlist]:
        option = await self.client.query_single(QUERY_PLAYLIST, playlist_id=playlist_id)

        return None if option is None else Playlist.from_object(option)

    async def delete_playlist(self, playlist_id: UUID) -> None:
        await self.client.query_single(DELETE_PLAYLIST, playlist_id=playlist_id)

    async def update_playlist(
        self, playlist_id: UUID, name: str, description: Optional[str], privacy_type: PrivacyType
    ) -> None:
        await self.client.query_single(
            UPDATE_PLAYLIST,
            playlist_id=playlist_id,
            name=name,
            description=description,
            privacy_type=privacy_type.value,
        )

    async def search_playlists(
        self, query: str, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT
    ) -> List[Playlist]:
        result = await self.client.query(
            SEARCH_PLAYLISTS, fts_query=query, offset=offset, limit=limit
        )

        return iter(result).map(Playlist.from_object).list()

    async def add_user_followed_playlists(self, user_id: UUID, ids: List[UUID]) -> None:
        await self.client.query_single(ADD_USER_FOLLOWED_PLAYLISTS, user_id=user_id, ids=ids)

    async def remove_user_followed_playlists(self, user_id: UUID, ids: List[UUID]) -> None:
        await self.client.query_single(REMOVE_USER_FOLLOWED_PLAYLISTS, user_id=user_id, ids=ids)

    async def query_playlist_privacy(self, playlist_id: UUID) -> Optional[PlaylistPrivacy]:
        option = await self.client.query_single(QUERY_PLAYLIST_PRIVACY, playlist_id=playlist_id)

        return None if option is None else PlaylistPrivacy.from_object(option)

    async def query_playlist_tracks(
        self,
        playlist_id: UUID,
        offset: int = DEFAULT_OFFSET,
        limit: int = DEFAULT_LIMIT,
    ) -> Optional[Counted[PositionTrack]]:
        option = await self.client.query_single(
            QUERY_PLAYLIST_TRACKS, playlist_id=playlist_id, offset=offset, limit=limit
        )

        return (
            None
            if option is None
            else (
                iter(option.tracks).map(PositionTrack.from_object).list(),
                option.track_count,
            )
        )

    async def query_user(self, user_id: UUID) -> Optional[User]:
        option = await self.client.query_single(QUERY_USER, user_id=user_id)

        return None if option is None else User.from_object(option)

    async def insert_user(self, name: str, email: str, password_hash: str) -> Base:
        object = await self.client.query_single(
            INSERT_USER, name=name, email=email, password_hash=password_hash
        )

        return Base.from_object(object)

    async def update_user_password_hash(self, user_id: UUID, password_hash: str) -> None:
        await self.client.query_single(
            UPDATE_USER_PASSWORD_HASH, user_id=user_id, password_hash=password_hash
        )

    async def update_user_verified(self, user_id: UUID, verified: bool) -> None:
        await self.client.query_single(UPDATE_USER_VERIFIED, user_id=user_id, verified=verified)

    async def delete_user(self, user_id: UUID) -> None:
        await self.client.query_single(DELETE_USER, user_id=user_id)

    async def search_users(
        self, query: str, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT
    ) -> List[User]:
        result = await self.client.query(SEARCH_USERS, fts_query=query, offset=offset, limit=limit)

        return iter(result).map(User.from_object).list()

    async def query_user_tracks(
        self, user_id: UUID, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT
    ) -> Optional[Counted[Track]]:
        option = await self.client.query_single(
            QUERY_USER_TRACKS, user_id=user_id, offset=offset, limit=limit
        )

        return (
            None
            if option is None
            else (iter(option.tracks).map(Track.from_object).list(), option.track_count)
        )

    async def save_user_tracks(self, user_id: UUID, ids: List[UUID]) -> None:
        await self.client.query_single(SAVE_USER_TRACKS, user_id=user_id, ids=ids)

    async def remove_user_tracks(self, user_id: UUID, ids: List[UUID]) -> None:
        await self.client.query_single(REMOVE_USER_TRACKS, user_id=user_id, ids=ids)

    async def query_user_artists(
        self, user_id: UUID, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT
    ) -> Optional[Counted[Artist]]:
        option = await self.client.query_single(
            QUERY_USER_ARTISTS, user_id=user_id, offset=offset, limit=limit
        )

        return (
            None
            if option is None
            else (
                iter(option.artists).map(Artist.from_object).list(),
                option.artist_count,
            )
        )

    async def save_user_artists(self, user_id: UUID, ids: List[UUID]) -> None:
        await self.client.query_single(SAVE_USER_ARTISTS, user_id=user_id, ids=ids)

    async def remove_user_artists(self, user_id: UUID, ids: List[UUID]) -> None:
        await self.client.query_single(REMOVE_USER_ARTISTS, user_id=user_id, ids=ids)

    async def query_user_albums(
        self, user_id: UUID, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT
    ) -> Optional[Counted[Album]]:
        option = await self.client.query_single(
            QUERY_USER_ALBUMS, user_id=user_id, offset=offset, limit=limit
        )

        return (
            None
            if option is None
            else (iter(option.albums).map(Album.from_object).list(), option.album_count)
        )

    async def save_user_albums(self, user_id: UUID, ids: List[UUID]) -> None:
        await self.client.query_single(SAVE_USER_ALBUMS, user_id=user_id, ids=ids)

    async def remove_user_albums(self, user_id: UUID, ids: List[UUID]) -> None:
        await self.client.query_single(REMOVE_USER_ALBUMS, user_id=user_id, ids=ids)

    async def query_user_playlists(
        self, user_id: UUID, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT
    ) -> Optional[Counted[Playlist]]:
        option = await self.client.query_single(
            QUERY_USER_PLAYLISTS, user_id=user_id, offset=offset, limit=limit
        )

        return (
            None
            if option is None
            else (
                iter(option.playlists).map(Playlist.from_object).list(),
                option.playlist_count,
            )
        )

    async def query_user_followed_playlists(
        self, user_id: UUID, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT
    ) -> Optional[Counted[Playlist]]:
        option = await self.client.query_single(
            QUERY_USER_FOLLOWED_PLAYLISTS, user_id=user_id, offset=offset, limit=limit
        )

        return (
            None
            if option is None
            else (
                iter(option.followed_playlists).map(Playlist.from_object).list(),
                option.followed_playlist_count,
            )
        )

    async def query_user_streams(
        self, user_id: UUID, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT
    ) -> Optional[Counted[Stream]]:
        option = await self.client.query_single(
            QUERY_USER_STREAMS, user_id=user_id, offset=offset, limit=limit
        )

        return (
            None
            if option is None
            else (
                iter(option.streams).map(Stream.from_object).list(),
                option.stream_count,
            )
        )

    async def query_user_followers(
        self, user_id: UUID, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT
    ) -> Optional[Counted[User]]:
        option = await self.client.query_single(
            QUERY_USER_FOLLOWERS, user_id=user_id, offset=offset, limit=limit
        )

        return (
            None
            if option is None
            else (
                iter(option.followers).map(User.from_object).list(),
                option.follower_count,
            )
        )

    async def query_user_following(
        self, user_id: UUID, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT
    ) -> Optional[Counted[User]]:
        option = await self.client.query_single(
            QUERY_USER_FOLLOWING, user_id=user_id, offset=offset, limit=limit
        )

        return (
            None
            if option is None
            else (
                iter(option.following).map(User.from_object).list(),
                option.following_count,
            )
        )

    async def add_user_following(self, user_id: UUID, ids: List[UUID]) -> None:
        await self.client.query_single(ADD_USER_FOLLOWING, user_id=user_id, ids=ids)

    async def remove_user_following(self, user_id: UUID, ids: List[UUID]) -> None:
        await self.client.query_single(REMOVE_USER_FOLLOWING, user_id=user_id, ids=ids)

    async def query_user_friends(
        self, user_id: UUID, offset: int = DEFAULT_OFFSET, limit: int = DEFAULT_LIMIT
    ) -> Optional[Counted[User]]:
        option = await self.client.query_single(
            QUERY_USER_FRIENDS, user_id=user_id, offset=offset, limit=limit
        )

        return (
            None
            if option is None
            else (
                iter(option.friends).map(User.from_object).list(),
                option.friend_count,
            )
        )

    async def query_user_friends_essential(self, user_id: UUID) -> Optional[Set[UUID]]:
        option = await self.client.query_single(QUERY_USER_FRIENDS_ESSENTIAL, user_id=user_id)

        return None if option is None else set(option.friends)

    async def check_user_friends(self, self_id: UUID, user_id: UUID) -> bool:
        option = await self.client.query_single(
            CHECK_USER_FRIENDS, self_id=self_id, user_id=user_id
        )

        return option is not None

    async def query_user_info(self, user_id: UUID) -> Optional[UserInfo]:
        option = await self.client.query_single(QUERY_USER_INFO, user_id=user_id)

        return None if option is None else UserInfo.from_object(option)

    async def query_user_info_by_email(self, email: str) -> Optional[UserInfo]:
        option = await self.client.query_single(QUERY_USER_INFO_BY_EMAIL, email=email)

        return None if option is None else UserInfo.from_object(option)

    async def query_user_settings(self, user_id: UUID) -> Optional[UserSettings]:
        option = await self.client.query_single(QUERY_USER_SETTINGS, user_id=user_id)

        return None if option is None else UserSettings.from_object(option)

    async def update_user_settings(
        self,
        user_id: UUID,
        name: str,
        explicit: bool,
        autoplay: bool,
        platform: Platform,
        privacy_type: PrivacyType,
    ) -> None:
        await self.client.query_single(
            UPDATE_USER_SETTINGS,
            user_id=user_id,
            name=name,
            explicit=explicit,
            autoplay=autoplay,
            platform=platform.value,
            privacy_type=privacy_type.value,
        )

    async def query_statistics(self) -> Statistics:
        object = await self.client.query_required_single(QUERY_STATISTICS)

        return Statistics.from_object(object)

    async def update_user_discord_id(self, user_id: UUID, discord_id: Optional[str]) -> None:
        await self.client.query_single(
            UPDATE_USER_DISCORD_ID, user_id=user_id, discord_id=discord_id
        )

    async def query_user_by_discord_id(self, discord_id: str) -> Optional[User]:
        option = await self.client.query_single(QUERY_USER_BY_DISCORD_ID, discord_id=discord_id)

        return None if option is None else User.from_object(option)

    async def update_user_secret(self, user_id: UUID, secret: Optional[str]) -> None:
        await self.client.query_single(UPDATE_USER_SECRET, user_id=user_id, secret=secret)

    async def query_user_privacy(self, user_id: UUID) -> Optional[UserPrivacy]:
        option = await self.client.query_single(QUERY_USER_PRIVACY, user_id=user_id)

        return None if option is None else UserPrivacy.from_object(option)

    async def query_client(self, client_id: UUID) -> Optional[Client]:
        option = await self.client.query_single(QUERY_CLIENT, client_id=client_id)

        return None if option is None else Client.from_object(option)

    async def query_client_info(self, client_id: UUID) -> Optional[ClientInfo]:
        option = await self.client.query_single(QUERY_CLIENT_INFO, client_id=client_id)

        return None if option is None else ClientInfo.from_object(option)

    async def insert_client(
        self, name: str, description: Optional[str], secret_hash: str, creator_id: UUID
    ) -> Base:
        object = await self.client.query_single(
            INSERT_CLIENT,
            name=name,
            description=description,
            secret_hash=secret_hash,
            creator_id=creator_id,
        )

        return Base.from_object(object)

    async def update_client(self, client_id: UUID, name: str, description: Optional[str]) -> None:
        await self.client.query_single(
            UPDATE_CLIENT, client_id=client_id, name=name, description=description
        )

    async def delete_client(self, client_id: UUID) -> None:
        await self.client.query_single(DELETE_CLIENT, client_id=client_id)

    async def update_client_secret_hash(self, client_id: UUID, secret_hash: str) -> None:
        await self.client.query_single(
            UPDATE_CLIENT_SECRET_HASH, client_id=client_id, secret_hash=secret_hash
        )
