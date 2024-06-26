from uuid import UUID

from async_extensions.paths import Path
from fastapi.responses import FileResponse

from melody.kit.code import generate_code_for_uri
from melody.kit.core import config, database, v1
from melody.kit.dependencies.common import LimitDependency, OffsetDependency
from melody.kit.dependencies.request_urls import RequestURLDependency
from melody.kit.enums import EntityType, Tag
from melody.kit.errors.users import UserImageNotFound, UserNotFound
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
    UserTracks,
    UserTracksData,
)
from melody.kit.tokens.dependencies import TokenDependency
from melody.kit.uri import URI

__all__ = (
    "get_user",
    "get_user_link",
    "get_user_image",
    "get_user_tracks",
    "get_user_artists",
    "get_user_albums",
    "get_user_playlists",
    "get_user_followers",
    "get_user_following",
    "get_user_friends",
)


@v1.get(
    "/users/{user_id}",
    tags=[Tag.USERS],
    summary="Fetches the user.",
)
async def get_user(user_id: UUID) -> UserData:
    user = await database.query_user(user_id=user_id)

    if user is None:
        raise UserNotFound(user_id)

    return user.into_data()


@v1.get(
    "/users/{user_id}/link",
    tags=[Tag.USERS],
    summary="Fetches the user's link.",
)
async def get_user_link(user_id: UUID) -> FileResponse:
    uri = URI(type=EntityType.USER, id=user_id)

    path = await generate_code_for_uri(uri)

    return FileResponse(path)


CAN_NOT_FIND_USER_IMAGE = "can not find the image for the user with ID `{}`"
can_not_find_user_image = CAN_NOT_FIND_USER_IMAGE.format


@v1.get(
    "/users/{user_id}/image",
    tags=[Tag.USERS],
    summary="Fetches the user's image.",
)
async def get_user_image(user_id: UUID) -> FileResponse:
    uri = URI(type=EntityType.USER, id=user_id)

    path = Path(config.image.directory_path / uri.image_name)

    if not await path.exists():
        raise UserImageNotFound(user_id)

    return FileResponse(path)


@v1.get(
    "/users/{user_id}/tracks",
    tags=[Tag.USERS],
    summary="Fetches the user's saved tracks.",
)
async def get_user_tracks(
    user_id: UUID,
    request_url: RequestURLDependency,
    offset: OffsetDependency = config.offset.default,
    limit: LimitDependency = config.limit.default,
) -> UserTracksData:
    counted = await database.query_user_tracks(user_id=user_id, offset=offset, limit=limit)

    if counted is None:
        raise UserNotFound(user_id)

    items, count = counted

    user_tracks = UserTracks(
        items, Pagination.paginate(url=request_url, offset=offset, limit=limit, count=count)
    )

    return user_tracks.into_data()


@v1.get(
    "/users/{user_id}/artists",
    tags=[Tag.USERS],
    summary="Fetches the user's saved artists.",
)
async def get_user_artists(
    user_id: UUID,
    request_url: RequestURLDependency,
    offset: OffsetDependency = config.offset.default,
    limit: LimitDependency = config.limit.default,
) -> UserArtistsData:
    counted = await database.query_user_artists(user_id=user_id, offset=offset, limit=limit)

    if counted is None:
        raise UserNotFound(user_id)

    items, count = counted

    user_artists = UserArtists(
        items, Pagination.paginate(url=request_url, offset=offset, limit=limit, count=count)
    )

    return user_artists.into_data()


@v1.get(
    "/users/{user_id}/albums",
    tags=[Tag.USERS],
    summary="Fetches the user's saved albums.",
)
async def get_user_albums(
    user_id: UUID,
    request_url: RequestURLDependency,
    offset: OffsetDependency = config.offset.default,
    limit: LimitDependency = config.limit.default,
) -> UserAlbumsData:
    counted = await database.query_user_albums(user_id=user_id, offset=offset, limit=limit)

    if counted is None:
        raise UserNotFound(user_id)

    items, count = counted

    user_albums = UserAlbums(
        items, Pagination.paginate(url=request_url, offset=offset, limit=limit, count=count)
    )

    return user_albums.into_data()


@v1.get(
    "/users/{user_id}/playlists",
    tags=[Tag.USERS],
    summary="Fetches the user's playlists.",
)
async def get_user_playlists(
    user_id: UUID,
    context: TokenDependency,
    request_url: RequestURLDependency,
    offset: OffsetDependency = config.offset.default,
    limit: LimitDependency = config.limit.default,
) -> UserPlaylistsData:
    counted = await database.query_user_playlists(user_id=user_id, offset=offset, limit=limit)

    if counted is None:
        raise UserNotFound(user_id)

    items, count = counted

    user_playlists = UserPlaylists(
        items, Pagination.paginate(url=request_url, offset=offset, limit=limit, count=count)
    )

    return user_playlists.into_data()


@v1.get(
    "/users/{user_id}/playlists/followed",
    tags=[Tag.USERS],
    summary="Fetches the user's followed playlists.",
)
async def get_user_followed_playlists(
    user_id: UUID,
    context: TokenDependency,
    request_url: RequestURLDependency,
    offset: OffsetDependency = config.offset.default,
    limit: LimitDependency = config.limit.default,
) -> UserFollowedPlaylistsData:
    counted = await database.query_user_followed_playlists(
        user_id=user_id, offset=offset, limit=limit
    )

    if counted is None:
        raise UserNotFound(user_id)

    items, count = counted

    user_followed_playlists = UserFollowedPlaylists(
        items, Pagination.paginate(url=request_url, offset=offset, limit=limit, count=count)
    )

    return user_followed_playlists.into_data()


@v1.get(
    "/users/{user_id}/followers",
    tags=[Tag.USERS],
    summary="Fetches the user's followers.",
)
async def get_user_followers(
    user_id: UUID,
    context: TokenDependency,
    request_url: RequestURLDependency,
    offset: OffsetDependency = config.offset.default,
    limit: LimitDependency = config.limit.default,
) -> UserFollowersData:
    counted = await database.query_user_followers(user_id=user_id, offset=offset, limit=limit)

    if counted is None:
        raise UserNotFound(user_id)

    items, count = counted

    user_followers = UserFollowers(
        items, Pagination.paginate(url=request_url, offset=offset, limit=limit, count=count)
    )

    return user_followers.into_data()


@v1.get(
    "/users/{user_id}/following",
    tags=[Tag.USERS],
    summary="Fetches the user's following.",
)
async def get_user_following(
    user_id: UUID,
    context: TokenDependency,
    request_url: RequestURLDependency,
    offset: OffsetDependency = config.offset.default,
    limit: LimitDependency = config.limit.default,
) -> UserFollowingData:
    counted = await database.query_user_following(user_id=user_id, offset=offset, limit=limit)

    if counted is None:
        raise UserNotFound(user_id)

    items, count = counted

    user_following = UserFollowing(
        items, Pagination.paginate(url=request_url, offset=offset, limit=limit, count=count)
    )

    return user_following.into_data()


@v1.get(
    "/users/{user_id}/friends",
    tags=[Tag.USERS],
    summary="Fetches the user's friends.",
)
async def get_user_friends(
    user_id: UUID,
    context: TokenDependency,
    request_url: RequestURLDependency,
    offset: OffsetDependency = config.offset.default,
    limit: LimitDependency = config.limit.default,
) -> UserFriendsData:
    counted = await database.query_user_friends(user_id=user_id, offset=offset, limit=limit)

    if counted is None:
        raise UserNotFound(user_id)

    items, count = counted

    user_friends = UserFriends(
        items, Pagination.paginate(url=request_url, offset=offset, limit=limit, count=count)
    )

    return user_friends.into_data()
