from uuid import UUID

from fastapi import Depends, status
from fastapi.responses import FileResponse
from iters import iter

from melody.kit.core import database, v1
from melody.kit.dependencies import token_dependency
from melody.kit.enums import URIType
from melody.kit.errors import Error, ErrorCode
from melody.kit.models.album import album_into_data
from melody.kit.models.artist import artist_into_data
from melody.kit.models.playlist import playlist_into_data
from melody.kit.models.track import track_into_data
from melody.kit.models.user import (
    UserAlbumsData,
    UserArtistsData,
    UserData,
    UserFollowersData,
    UserFollowingData,
    UserFriendsData,
    UserPlaylistsData,
    UserStreamsData,
    UserTracksData,
    user_into_data,
)
from melody.kit.tags import ALBUMS, ARTISTS, LINKS, PLAYLISTS, SELF, TRACKS, USERS
from melody.kit.uri import URI

__all__ = (
    "get_self",
    "get_self_link",
    "get_self_tracks",
    "get_self_artists",
    "get_self_albums",
    "get_self_playlists",
    "get_self_streams",
    "get_self_friends",
    "get_self_followers",
    "get_self_following",
)

CAN_NOT_FIND_USER = "can not find the user with ID `{}`"


@v1.get(
    "/me",
    tags=[SELF],
    summary="Fetch self user.",
)
async def get_self(user_id: UUID = Depends(token_dependency)) -> UserData:
    user = await database.query_user(user_id)

    if user is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return user.into_data()


@v1.get(
    "/me/link",
    tags=[SELF, LINKS],
    summary="Fetch self user link.",
)
async def get_self_link(user_id: UUID = Depends(token_dependency)) -> FileResponse:
    uri = URI(type=URIType.USER, id=user_id)

    path = await uri.create_link()

    return FileResponse(path)


@v1.get(
    "/me/tracks",
    tags=[SELF, TRACKS],
    summary="Fetch self user tracks.",
)
async def get_self_tracks(user_id: UUID = Depends(token_dependency)) -> UserTracksData:
    tracks = await database.query_user_tracks(user_id)

    if tracks is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return iter(tracks).map(track_into_data).list()


@v1.get(
    "/me/artists",
    tags=[SELF, ARTISTS],
    summary="Fetch self user artists.",
)
async def get_self_artists(user_id: UUID = Depends(token_dependency)) -> UserArtistsData:
    artists = await database.query_user_artists(user_id)

    if artists is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return iter(artists).map(artist_into_data).list()


@v1.get(
    "/me/albums",
    tags=[SELF, ALBUMS],
    summary="Fetch self user albums.",
)
async def get_self_albums(user_id: UUID = Depends(token_dependency)) -> UserAlbumsData:
    albums = await database.query_user_albums(user_id)

    if albums is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return iter(albums).map(album_into_data).list()


@v1.get(
    "/me/playlists",
    tags=[SELF, PLAYLISTS],
    summary="Fetch self user playlists.",
)
async def get_self_playlists(user_id: UUID = Depends(token_dependency)) -> UserPlaylistsData:
    playlists = await database.query_user_playlists(user_id)

    if playlists is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return iter(playlists).map(playlist_into_data).list()


@v1.get(
    "/me/streams",
    tags=[SELF, TRACKS],
    summary="Fetch self user streams.",
)
async def get_self_streams(user_id: UUID = Depends(token_dependency)) -> UserStreamsData:
    streams = await database.query_user_streams(user_id)

    if streams is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return iter(streams).map(track_into_data).list()


@v1.get(
    "/me/friends",
    tags=[SELF, USERS],
    summary="Fetch self user friends.",
)
async def get_self_friends(user_id: UUID = Depends(token_dependency)) -> UserFriendsData:
    friends = await database.query_user_friends(user_id)

    if friends is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return iter(friends).map(user_into_data).list()


@v1.get(
    "/me/followers",
    tags=[SELF, USERS],
    summary="Fetch self user followers.",
)
async def get_self_followers(user_id: UUID = Depends(token_dependency)) -> UserFollowersData:
    followers = await database.query_user_followers(user_id)

    if followers is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return iter(followers).map(user_into_data).list()


@v1.get(
    "/me/following",
    tags=[SELF, USERS],
    summary="Fetch self user following.",
)
async def get_self_following(user_id: UUID = Depends(token_dependency)) -> UserFollowingData:
    following = await database.query_user_following(user_id)

    if following is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return iter(following).map(user_into_data).list()