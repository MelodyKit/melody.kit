from typing import List
from uuid import UUID

from fastapi import Body, Depends, File, UploadFile
from fastapi.responses import FileResponse
from iters import iter

from melody.kit.core import config, database, v1
from melody.kit.dependencies import token_dependency
from melody.kit.enums import EntityType
from melody.kit.errors import NotFound, ValidationError
from melody.kit.link import generate_code_for_uri
from melody.kit.models.album import album_into_data
from melody.kit.models.artist import artist_into_data
from melody.kit.models.playlist import partial_playlist_into_data
from melody.kit.models.streams import user_stream_into_data
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
from melody.kit.tags import ALBUMS, ARTISTS, IMAGES, LINKS, PLAYLISTS, SELF, TRACKS, USERS
from melody.kit.uri import URI
from melody.shared.constants import IMAGE_TYPE
from melody.shared.image import check_image_type, validate_and_save_image

__all__ = (
    "get_self",
    "get_self_link",
    "get_self_image",
    "change_self_image",
    "get_self_tracks",
    "save_self_tracks",
    "remove_self_tracks",
    "get_self_artists",
    "save_self_artists",
    "remove_self_artists",
    "get_self_albums",
    "save_self_albums",
    "remove_self_albums",
    "get_self_playlists",
    "get_self_streams",
    "get_self_friends",
    "get_self_followers",
    "get_self_following",
)

CAN_NOT_FIND_USER = "can not find the user with ID `{}`"
CAN_NOT_FIND_USER_IMAGE = "can not find the image for the user with ID `{}`"


@v1.get(
    "/me",
    tags=[SELF],
    summary="Fetch self user.",
)
async def get_self(user_id: UUID = Depends(token_dependency)) -> UserData:
    user = await database.query_user(user_id)

    if user is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    return user.into_data()


@v1.get(
    "/me/link",
    tags=[SELF, LINKS],
    summary="Fetch self user link.",
)
async def get_self_link(user_id: UUID = Depends(token_dependency)) -> FileResponse:
    uri = URI(type=EntityType.USER, id=user_id)

    path = await generate_code_for_uri(uri)

    return FileResponse(path)


@v1.get(
    "/me/image",
    tags=[SELF, IMAGES],
    summary="Fetch self user image.",
)
async def get_self_image(user_id: UUID = Depends(token_dependency)) -> FileResponse:
    uri = URI(type=EntityType.USER, id=user_id)

    path = config.images / uri.image_name

    if not path.exists():
        raise NotFound(CAN_NOT_FIND_USER_IMAGE.format(user_id))

    return FileResponse(path)


EXPECTED_IMAGE_TYPE = f"expected `{IMAGE_TYPE}` image type"
EXPECTED_SQUARE_IMAGE = "expected square image"


@v1.put(
    "/me/image",
    tags=[SELF, IMAGES],
    summary="Changes self user image.",
)
async def change_self_image(
    image: UploadFile = File(), user_id: UUID = Depends(token_dependency)
) -> None:
    if not check_image_type(image):
        raise ValidationError(EXPECTED_IMAGE_TYPE)

    uri = URI(type=EntityType.USER, id=user_id)

    path = config.images / uri.image_name

    if not await validate_and_save_image(image, path):
        raise ValidationError(EXPECTED_SQUARE_IMAGE)


@v1.get(
    "/me/tracks",
    tags=[SELF, TRACKS],
    summary="Fetch self user tracks.",
)
async def get_self_tracks(user_id: UUID = Depends(token_dependency)) -> UserTracksData:
    tracks = await database.query_user_tracks(user_id)

    if tracks is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    return iter(tracks).map(track_into_data).list()


@v1.put(
    "/me/tracks",
    tags=[SELF, TRACKS],
    summary="Save self user tracks.",
)
async def save_self_tracks(
    user_id: UUID = Depends(token_dependency), ids: List[UUID] = Body()
) -> None:
    await database.save_user_tracks(user_id=user_id, ids=ids)


@v1.delete(
    "/me/tracks",
    tags=[SELF, TRACKS],
    summary="Remove self user tracks.",
)
async def remove_self_tracks(
    user_id: UUID = Depends(token_dependency), ids: List[UUID] = Body()
) -> None:
    await database.remove_user_tracks(user_id=user_id, ids=ids)


@v1.get(
    "/me/artists",
    tags=[SELF, ARTISTS],
    summary="Fetch self user artists.",
)
async def get_self_artists(user_id: UUID = Depends(token_dependency)) -> UserArtistsData:
    artists = await database.query_user_artists(user_id)

    if artists is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    return iter(artists).map(artist_into_data).list()


@v1.put(
    "/me/artists",
    tags=[SELF, ARTISTS],
    summary="Save self user artists.",
)
async def save_self_artists(
    user_id: UUID = Depends(token_dependency), ids: List[UUID] = Body()
) -> None:
    await database.save_user_artists(user_id=user_id, ids=ids)


@v1.delete(
    "/me/artists",
    tags=[SELF, ARTISTS],
    summary="Remove self user artists.",
)
async def remove_self_artists(
    user_id: UUID = Depends(token_dependency), ids: List[UUID] = Body()
) -> None:
    await database.remove_user_artists(user_id=user_id, ids=ids)


@v1.get(
    "/me/albums",
    tags=[SELF, ALBUMS],
    summary="Fetch self user albums.",
)
async def get_self_albums(user_id: UUID = Depends(token_dependency)) -> UserAlbumsData:
    albums = await database.query_user_albums(user_id)

    if albums is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    return iter(albums).map(album_into_data).list()


@v1.put(
    "/me/albums",
    tags=[SELF, ALBUMS],
    summary="Save self user albums.",
)
async def save_self_albums(
    user_id: UUID = Depends(token_dependency), ids: List[UUID] = Body()
) -> None:
    await database.save_user_albums(user_id=user_id, ids=ids)


@v1.delete(
    "/me/albums",
    tags=[SELF, ALBUMS],
    summary="Remove self user albums.",
)
async def remove_self_albums(
    user_id: UUID = Depends(token_dependency), ids: List[UUID] = Body()
) -> None:
    await database.remove_user_albums(user_id=user_id, ids=ids)


@v1.get(
    "/me/playlists",
    tags=[SELF, PLAYLISTS],
    summary="Fetch self user playlists.",
)
async def get_self_playlists(user_id: UUID = Depends(token_dependency)) -> UserPlaylistsData:
    playlists = await database.query_user_playlists(user_id)

    if playlists is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    return iter(playlists).map(partial_playlist_into_data).list()


@v1.get(
    "/me/streams",
    tags=[SELF, TRACKS],
    summary="Fetch self user streams.",
)
async def get_self_streams(user_id: UUID = Depends(token_dependency)) -> UserStreamsData:
    streams = await database.query_user_streams(user_id)

    if streams is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    return iter(streams).map(user_stream_into_data).list()


@v1.get(
    "/me/friends",
    tags=[SELF, USERS],
    summary="Fetch self user friends.",
)
async def get_self_friends(user_id: UUID = Depends(token_dependency)) -> UserFriendsData:
    friends = await database.query_user_friends(user_id)

    if friends is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    return iter(friends).map(user_into_data).list()


@v1.get(
    "/me/followers",
    tags=[SELF, USERS],
    summary="Fetch self user followers.",
)
async def get_self_followers(user_id: UUID = Depends(token_dependency)) -> UserFollowersData:
    followers = await database.query_user_followers(user_id)

    if followers is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    return iter(followers).map(user_into_data).list()


@v1.get(
    "/me/following",
    tags=[SELF, USERS],
    summary="Fetch self user following.",
)
async def get_self_following(user_id: UUID = Depends(token_dependency)) -> UserFollowingData:
    following = await database.query_user_following(user_id)

    if following is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    return iter(following).map(user_into_data).list()
