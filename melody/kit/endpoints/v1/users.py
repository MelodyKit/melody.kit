from typing import Optional
from uuid import UUID

from fastapi import Depends, Query
from fastapi.responses import FileResponse
from iters.iters import iter
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
from melody.kit.dependencies import request_url_dependency
from melody.kit.enums import EntityType
from melody.kit.errors import NotFound
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
from melody.kit.oauth2 import optional_token_dependency
from melody.kit.privacy import (
    check_user_accessible_dependency,
    create_partial_playlist_accessible_predicate,
    create_playlist_accessible_predicate,
    create_user_accessible_predicate,
)
from melody.kit.tags import ALBUMS, ARTISTS, IMAGES, LINKS, PLAYLISTS, TRACKS, USERS
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

CAN_NOT_FIND_USER = "can not find the user with ID `{}`"
can_not_find_user = CAN_NOT_FIND_USER.format


@v1.get(
    "/users/{user_id}",
    tags=[USERS],
    summary="Fetches the user with the given ID.",
    dependencies=[Depends(check_user_accessible_dependency)],
)
async def get_user(user_id: UUID) -> UserData:
    user = await database.query_user(user_id=user_id)

    if user is None:
        raise NotFound(can_not_find_user(user_id))

    return user.into_data()


@v1.get(
    "/users/{user_id}/link",
    tags=[USERS, LINKS],
    summary="Fetches the user link with the given ID.",
)
async def get_user_link(user_id: UUID) -> FileResponse:
    uri = URI(type=EntityType.USER, id=user_id)

    path = await generate_code_for_uri(uri)

    return FileResponse(path)


CAN_NOT_FIND_USER_IMAGE = "can not find the image for the user with ID `{}`"
can_not_find_user_image = CAN_NOT_FIND_USER_IMAGE.format


@v1.get(
    "/users/{user_id}/image",
    tags=[USERS, IMAGES],
    summary="Fetches the user image with the given ID.",
    dependencies=[Depends(check_user_accessible_dependency)],
)
async def get_user_image(user_id: UUID) -> FileResponse:
    uri = URI(type=EntityType.USER, id=user_id)

    path = config.images / uri.image_name

    if not path.exists():
        raise NotFound(can_not_find_user_image(user_id))

    return FileResponse(path)


@v1.get(
    "/users/{user_id}/tracks",
    tags=[USERS, TRACKS],
    summary="Fetches user tracks by the given ID.",
    dependencies=[Depends(check_user_accessible_dependency)],
)
async def get_user_tracks(
    user_id: UUID,
    url: URL = Depends(request_url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserTracksData:
    counted = await database.query_user_tracks(user_id=user_id, offset=offset, limit=limit)

    if counted is None:
        raise NotFound(can_not_find_user(user_id))

    items, count = counted

    user_tracks = UserTracks(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return user_tracks.into_data()


@v1.get(
    "/users/{user_id}/artists",
    tags=[USERS, ARTISTS],
    summary="Fetches user artists by the given ID.",
    dependencies=[Depends(check_user_accessible_dependency)],
)
async def get_user_artists(
    user_id: UUID,
    url: URL = Depends(request_url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserArtistsData:
    counted = await database.query_user_artists(user_id=user_id, offset=offset, limit=limit)

    if counted is None:
        raise NotFound(can_not_find_user(user_id))

    items, count = counted

    user_artists = UserArtists(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return user_artists.into_data()


@v1.get(
    "/users/{user_id}/albums",
    tags=[USERS, ALBUMS],
    summary="Fetches user albums by the given ID.",
    dependencies=[Depends(check_user_accessible_dependency)],
)
async def get_user_albums(
    user_id: UUID,
    url: URL = Depends(request_url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserAlbumsData:
    counted = await database.query_user_albums(user_id=user_id, offset=offset, limit=limit)

    if counted is None:
        raise NotFound(can_not_find_user(user_id))

    items, count = counted

    user_albums = UserAlbums(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return user_albums.into_data()


@v1.get(
    "/users/{user_id}/playlists",
    tags=[USERS, PLAYLISTS],
    summary="Fetches user playlists by the given ID.",
    dependencies=[Depends(check_user_accessible_dependency)],
)
async def get_user_playlists(
    user_id: UUID,
    self_id: Optional[UUID] = Depends(optional_token_dependency),
    url: URL = Depends(request_url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserPlaylistsData:
    counted = await database.query_user_playlists(user_id=user_id, offset=offset, limit=limit)

    if counted is None:
        raise NotFound(can_not_find_user(user_id))

    items, count = counted

    is_partial_playlist_accessible = await create_partial_playlist_accessible_predicate(
        user_id, self_id
    )

    items = iter(items).filter(is_partial_playlist_accessible).list()

    user_playlists = UserPlaylists(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return user_playlists.into_data()


@v1.get(
    "/users/{user_id}/playlists/followed",
    tags=[USERS, PLAYLISTS],
    summary="Fetches user followed playlists by the given ID.",
    dependencies=[Depends(check_user_accessible_dependency)],
)
async def get_user_followed_playlists(
    user_id: UUID,
    self_id: Optional[UUID] = Depends(optional_token_dependency),
    url: URL = Depends(request_url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserFollowedPlaylistsData:
    counted = await database.query_user_followed_playlists(
        user_id=user_id, offset=offset, limit=limit
    )

    if counted is None:
        raise NotFound(can_not_find_user(user_id))

    items, count = counted

    is_playlist_accessible = await create_playlist_accessible_predicate(self_id)

    items = iter(items).filter(is_playlist_accessible).list()

    user_followed_playlists = UserFollowedPlaylists(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return user_followed_playlists.into_data()


@v1.get(
    "/users/{user_id}/followers",
    tags=[USERS],
    summary="Fetches user followers by the given ID.",
    dependencies=[Depends(check_user_accessible_dependency)],
)
async def get_user_followers(
    user_id: UUID,
    self_id: Optional[UUID] = Depends(optional_token_dependency),
    url: URL = Depends(request_url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserFollowersData:
    counted = await database.query_user_followers(user_id=user_id, offset=offset, limit=limit)

    if counted is None:
        raise NotFound(can_not_find_user(user_id))

    items, count = counted

    is_user_accessible = await create_user_accessible_predicate(self_id)

    items = iter(items).filter(is_user_accessible).list()

    user_followers = UserFollowers(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return user_followers.into_data()


@v1.get(
    "/users/{user_id}/following",
    tags=[USERS],
    summary="Fetches user following by the given ID.",
    dependencies=[Depends(check_user_accessible_dependency)],
)
async def get_user_following(
    user_id: UUID,
    self_id: Optional[UUID] = Depends(optional_token_dependency),
    url: URL = Depends(request_url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserFollowingData:
    counted = await database.query_user_following(user_id=user_id, offset=offset, limit=limit)

    if counted is None:
        raise NotFound(can_not_find_user(user_id))

    items, count = counted

    is_user_accessible = await create_user_accessible_predicate(self_id)

    items = iter(items).filter(is_user_accessible).list()

    user_following = UserFollowing(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return user_following.into_data()


INACCESSIBLE_FRIENDS = "the friends of the user with ID `{}` are inaccessible"
inaccessible_friends = INACCESSIBLE_FRIENDS.format


@v1.get(
    "/users/{user_id}/friends",
    tags=[USERS],
    summary="Fetches user friends by the given ID.",
    dependencies=[Depends(check_user_accessible_dependency)],
)
async def get_user_friends(
    user_id: UUID,
    self_id: Optional[UUID] = Depends(optional_token_dependency),
    url: URL = Depends(request_url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserFriendsData:
    counted = await database.query_user_friends(user_id=user_id, offset=offset, limit=limit)

    if counted is None:
        raise NotFound(can_not_find_user(user_id))

    items, count = counted

    is_user_accessible = await create_user_accessible_predicate(self_id)

    items = iter(items).filter(is_user_accessible).list()

    user_friends = UserFriends(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return user_friends.into_data()
