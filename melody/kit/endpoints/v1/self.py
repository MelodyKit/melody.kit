from typing import List, Optional
from uuid import UUID

from fastapi import Body, Depends, File, Query, UploadFile
from fastapi.responses import FileResponse
from yarl import URL

from melody.kit.code import generate_code_for_uri
from melody.kit.constants import (
    DEFAULT_LIMIT,
    DEFAULT_OFFSET,
    MAX_LIMIT,
    MIN_LIMIT,
    MIN_OFFSET,
)
from melody.kit.core import config, database, v1
from melody.kit.dependencies import access_token_dependency, url_dependency
from melody.kit.enums import EntityType, Platform, PrivacyType
from melody.kit.errors import NotFound, ValidationError
from melody.kit.models.pagination import Pagination
from melody.kit.models.user import (
    UserAlbums,
    UserAlbumsData,
    UserArtists,
    UserArtistsData,
    UserData,
    UserFollowedPlaylists,
    UserFollowedPlaylistsData,
    UserFollowers,
    UserFollowersData,
    UserFollowing,
    UserFollowingData,
    UserFriends,
    UserFriendsData,
    UserPlaylists,
    UserPlaylistsData,
    UserStreams,
    UserStreamsData,
    UserTracks,
    UserTracksData,
)
from melody.kit.models.user_settings import UserSettingsData
from melody.kit.tags import (
    ALBUMS,
    ARTISTS,
    IMAGES,
    LINKS,
    PLAYLISTS,
    SELF,
    SETTINGS,
    TRACKS,
    USERS,
)
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
    "add_self_following",
    "remove_self_following",
    "get_self_followed_playlists",
    "get_self_settings",
    "update_self_settings",
)

CAN_NOT_FIND_USER = "can not find the user with ID `{}`"
CAN_NOT_FIND_USER_IMAGE = "can not find the image for the user with ID `{}`"


@v1.get(
    "/me",
    tags=[SELF],
    summary="Fetch self user.",
)
async def get_self(user_id: UUID = Depends(access_token_dependency)) -> UserData:
    user = await database.query_user(user_id=user_id)

    if user is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    return user.into_data()


@v1.get(
    "/me/link",
    tags=[SELF, LINKS],
    summary="Fetch self user link.",
)
async def get_self_link(
    user_id: UUID = Depends(access_token_dependency),
) -> FileResponse:
    uri = URI(type=EntityType.USER, id=user_id)

    path = await generate_code_for_uri(uri)

    return FileResponse(path)


@v1.get(
    "/me/image",
    tags=[SELF, IMAGES],
    summary="Fetch self user image.",
)
async def get_self_image(
    user_id: UUID = Depends(access_token_dependency),
) -> FileResponse:
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
    image: UploadFile = File(), user_id: UUID = Depends(access_token_dependency)
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
async def get_self_tracks(
    user_id: UUID = Depends(access_token_dependency),
    url: URL = Depends(url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserTracksData:
    counted = await database.query_user_tracks(user_id=user_id, offset=offset, limit=limit)

    if counted is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    items, count = counted

    self_tracks = UserTracks(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return self_tracks.into_data()


@v1.put(
    "/me/tracks",
    tags=[SELF, TRACKS],
    summary="Save self user tracks.",
)
async def save_self_tracks(
    user_id: UUID = Depends(access_token_dependency), ids: List[UUID] = Body()
) -> None:
    await database.save_user_tracks(user_id=user_id, ids=ids)


@v1.delete(
    "/me/tracks",
    tags=[SELF, TRACKS],
    summary="Remove self user tracks.",
)
async def remove_self_tracks(
    user_id: UUID = Depends(access_token_dependency), ids: List[UUID] = Body()
) -> None:
    await database.remove_user_tracks(user_id=user_id, ids=ids)


@v1.get(
    "/me/artists",
    tags=[SELF, ARTISTS],
    summary="Fetch self user artists.",
)
async def get_self_artists(
    user_id: UUID = Depends(access_token_dependency),
    url: URL = Depends(url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserArtistsData:
    counted = await database.query_user_artists(user_id=user_id)

    if counted is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    items, count = counted

    self_artists = UserArtists(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return self_artists.into_data()


@v1.put(
    "/me/artists",
    tags=[SELF, ARTISTS],
    summary="Save self user artists.",
)
async def save_self_artists(
    user_id: UUID = Depends(access_token_dependency), ids: List[UUID] = Body()
) -> None:
    await database.save_user_artists(user_id=user_id, ids=ids)


@v1.delete(
    "/me/artists",
    tags=[SELF, ARTISTS],
    summary="Remove self user artists.",
)
async def remove_self_artists(
    user_id: UUID = Depends(access_token_dependency), ids: List[UUID] = Body()
) -> None:
    await database.remove_user_artists(user_id=user_id, ids=ids)


@v1.get(
    "/me/albums",
    tags=[SELF, ALBUMS],
    summary="Fetch self user albums.",
)
async def get_self_albums(
    user_id: UUID = Depends(access_token_dependency),
    url: URL = Depends(url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserAlbumsData:
    counted = await database.query_user_albums(user_id=user_id)

    if counted is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    items, count = counted

    self_albums = UserAlbums(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return self_albums.into_data()


@v1.put(
    "/me/albums",
    tags=[SELF, ALBUMS],
    summary="Save self user albums.",
)
async def save_self_albums(
    user_id: UUID = Depends(access_token_dependency), ids: List[UUID] = Body()
) -> None:
    await database.save_user_albums(user_id=user_id, ids=ids)


@v1.delete(
    "/me/albums",
    tags=[SELF, ALBUMS],
    summary="Remove self user albums.",
)
async def remove_self_albums(
    user_id: UUID = Depends(access_token_dependency), ids: List[UUID] = Body()
) -> None:
    await database.remove_user_albums(user_id=user_id, ids=ids)


@v1.get(
    "/me/playlists",
    tags=[SELF, PLAYLISTS],
    summary="Fetch self user playlists.",
)
async def get_self_playlists(
    user_id: UUID = Depends(access_token_dependency),
    url: URL = Depends(url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserPlaylistsData:
    counted = await database.query_user_playlists(user_id=user_id)

    if counted is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    items, count = counted

    self_playlists = UserPlaylists(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return self_playlists.into_data()


@v1.get(
    "/me/streams",
    tags=[SELF, TRACKS],
    summary="Fetch self user streams.",
)
async def get_self_streams(
    user_id: UUID = Depends(access_token_dependency),
    url: URL = Depends(url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserStreamsData:
    counted = await database.query_user_streams(user_id=user_id)

    if counted is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    items, count = counted

    self_streams = UserStreams(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return self_streams.into_data()


@v1.get(
    "/me/friends",
    tags=[SELF, USERS],
    summary="Fetch self user friends.",
)
async def get_self_friends(
    user_id: UUID = Depends(access_token_dependency),
    url: URL = Depends(url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserFriendsData:
    counted = await database.query_user_friends(user_id=user_id)

    if counted is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    items, count = counted

    self_friends = UserFriends(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return self_friends.into_data()


@v1.get(
    "/me/followers",
    tags=[SELF, USERS],
    summary="Fetch self user followers.",
)
async def get_self_followers(
    user_id: UUID = Depends(access_token_dependency),
    url: URL = Depends(url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserFollowersData:
    counted = await database.query_user_followers(user_id=user_id)

    if counted is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    items, count = counted

    self_followers = UserFollowers(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return self_followers.into_data()


@v1.get(
    "/me/following",
    tags=[SELF, USERS],
    summary="Fetch self user following.",
)
async def get_self_following(
    user_id: UUID = Depends(access_token_dependency),
    url: URL = Depends(url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserFollowingData:
    counted = await database.query_user_following(user_id=user_id)

    if counted is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    items, count = counted

    self_following = UserFollowing(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return self_following.into_data()


@v1.put(
    "/me/following",
    tags=[SELF, USERS],
    summary="Add users to self following.",
)
async def add_self_following(
    user_id: UUID = Depends(access_token_dependency), ids: List[UUID] = Body()
) -> None:
    await database.add_user_following(user_id=user_id, ids=ids)


@v1.delete(
    "/me/following",
    tags=[SELF, USERS],
    summary="Remove users from self following.",
)
async def remove_self_following(
    user_id: UUID = Depends(access_token_dependency), ids: List[UUID] = Body()
) -> None:
    await database.remove_user_following(user_id=user_id, ids=ids)


@v1.get(
    "/me/playlists/followed",
    tags=[SELF, PLAYLISTS],
    summary="Fetch self user followed playlists.",
)
async def get_self_followed_playlists(
    user_id: UUID = Depends(access_token_dependency),
    url: URL = Depends(url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserFollowedPlaylistsData:
    counted = await database.query_user_followed_playlists(user_id=user_id)

    if counted is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    items, count = counted

    self_followed_playlists = UserFollowedPlaylists(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return self_followed_playlists.into_data()


@v1.put(
    "/me/playlists/followed",
    tags=[SELF, PLAYLISTS],
    summary="Add playlists to self followed playlists.",
)
async def add_self_followed_playlists(
    user_id: UUID = Depends(access_token_dependency),
    ids: List[UUID] = Body(),
) -> None:
    await database.add_user_followed_playlists(user_id=user_id, ids=ids)


@v1.delete(
    "/me/playlists/followed",
    tags=[SELF, PLAYLISTS],
    summary="Remove playlists from self followed playlists.",
)
async def remove_self_followed_playlists(
    user_id: UUID = Depends(access_token_dependency),
    ids: List[UUID] = Body(),
) -> None:
    await database.remove_user_followed_playlists(user_id=user_id, ids=ids)


@v1.get(
    "/me/settings",
    tags=[SELF, SETTINGS],
    summary="Fetch self settings.",
)
async def get_self_settings(
    user_id: UUID = Depends(access_token_dependency),
) -> UserSettingsData:
    self_settings = await database.query_user_settings(user_id=user_id)

    if self_settings is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    return self_settings.into_data()


@v1.put(
    "/me/settings",
    tags=[SELF, SETTINGS],
    summary="Update self settings.",
)
async def update_self_settings(
    user_id: UUID = Depends(access_token_dependency),
    name: Optional[str] = Body(default=None),
    explicit: Optional[bool] = Body(default=None),
    autoplay: Optional[bool] = Body(default=None),
    platform: Optional[Platform] = Body(default=None),
    privacy_type: Optional[PrivacyType] = Body(default=None),
) -> None:
    if (
        name is None
        and explicit is None
        and autoplay is None
        and platform is None
        and privacy_type is None
    ):
        return  # there is nothing to update

    settings = await database.query_user_settings(user_id=user_id)

    if settings is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    if name is None:
        name = settings.name

    if explicit is None:
        explicit = settings.is_explicit()

    if autoplay is None:
        autoplay = settings.is_autoplay()

    if platform is None:
        platform = settings.platform

    if privacy_type is None:
        privacy_type = settings.privacy_type

    await database.update_user_settings(
        user_id=user_id,
        name=name,
        explicit=explicit,
        autoplay=autoplay,
        platform=platform,
        privacy_type=privacy_type,
    )
