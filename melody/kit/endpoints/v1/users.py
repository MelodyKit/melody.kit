from typing import Optional
from uuid import UUID

from fastapi import Depends, Query
from fastapi.responses import FileResponse
from iters.iters import iter
from typing_aliases import Predicate
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
from melody.kit.dependencies import optional_access_token_dependency, request_url_dependency
from melody.kit.enums import EntityType
from melody.kit.errors import Forbidden, NotFound
from melody.kit.models.pagination import Pagination
from melody.kit.models.playlist import PartialPlaylist
from melody.kit.models.user import (
    User,
    UserAlbums,
    UserAlbumsData,
    UserArtists,
    UserArtistsData,
    UserData,
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
from melody.kit.privacy import (
    are_friends,
    is_playlist_accessible,
    is_playlist_public,
    is_user_accessible,
    is_user_public,
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
CAN_NOT_FIND_USER_IMAGE = "can not find the image for the user with ID `{}`"


@v1.get(
    "/users/{user_id}",
    tags=[USERS],
    summary="Fetches the user with the given ID.",
)
async def get_user(user_id: UUID) -> UserData:
    user = await database.query_user(user_id=user_id)

    if user is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

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


@v1.get(
    "/users/{user_id}/image",
    tags=[USERS, IMAGES],
    summary="Fetches the user image with the given ID.",
)
async def get_user_image(user_id: UUID) -> FileResponse:
    uri = URI(type=EntityType.USER, id=user_id)

    path = config.images / uri.image_name

    if not path.exists():
        raise NotFound(CAN_NOT_FIND_USER_IMAGE.format(user_id))

    return FileResponse(path)


INACCESSIBLE_TRACKS = "the tracks of the user with ID `{}` are inaccessible"
inaccessible_tracks = INACCESSIBLE_TRACKS.format


@v1.get(
    "/users/{user_id}/tracks",
    tags=[USERS, TRACKS],
    summary="Fetches user tracks by the given ID.",
)
async def get_user_tracks(
    user_id: UUID,
    user_id_option: Optional[UUID] = Depends(optional_access_token_dependency),
    url: URL = Depends(request_url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserTracksData:
    user = await database.query_user(user_id=user_id)

    if user is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    if user_id_option is None:
        accessible = is_user_public(user)

    else:
        friends = await are_friends(user_id_option, user_id)

        accessible = is_user_accessible(user_id_option, user, friends)

    if not accessible:
        raise Forbidden(inaccessible_tracks(user_id))

    counted = await database.query_user_tracks(user_id=user_id)

    if counted is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    items, count = counted

    user_tracks = UserTracks(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return user_tracks.into_data()


INACCESSIBLE_ARTISTS = "the artists of the user with ID `{}` are inaccessible"


@v1.get(
    "/users/{user_id}/artists",
    tags=[USERS, ARTISTS],
    summary="Fetches user artists by the given ID.",
)
async def get_user_artists(
    user_id: UUID,
    user_id_option: Optional[UUID] = Depends(optional_access_token_dependency),
    url: URL = Depends(request_url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserArtistsData:
    user = await database.query_user(user_id=user_id)

    if user is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    if user_id_option is None:
        accessible = is_user_public(user)

    else:
        friends = await are_friends(user_id_option, user_id)

        accessible = is_user_accessible(user_id_option, user, friends)

    if not accessible:
        raise Forbidden(INACCESSIBLE_ARTISTS.format(user_id))

    counted = await database.query_user_artists(user_id=user_id)

    if counted is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    items, count = counted

    user_artists = UserArtists(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return user_artists.into_data()


INACCESSIBLE_ALBUMS = "the albums of the user with ID `{}` are inaccessible"


@v1.get(
    "/users/{user_id}/albums",
    tags=[USERS, ALBUMS],
    summary="Fetches user albums by the given ID.",
)
async def get_user_albums(
    user_id: UUID,
    user_id_option: Optional[UUID] = Depends(optional_access_token_dependency),
    url: URL = Depends(request_url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserAlbumsData:
    user = await database.query_user(user_id=user_id)

    if user is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    if user_id_option is None:
        accessible = is_user_public(user)

    else:
        friends = await are_friends(user_id_option, user_id)

        accessible = is_user_accessible(user_id_option, user, friends)

    if not accessible:
        raise Forbidden(INACCESSIBLE_ALBUMS.format(user_id))

    counted = await database.query_user_albums(user_id=user_id)

    if counted is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    items, count = counted

    user_albums = UserAlbums(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return user_albums.into_data()


INACCESSIBLE_PLAYLISTS = "the playlists of the user with ID `{}` are inaccessible"


def is_playlist_accessible_by(
    self_id: UUID, user: User, friends: bool
) -> Predicate[PartialPlaylist]:
    def is_playlist_accessible_predicate(playlist: PartialPlaylist) -> bool:
        return is_playlist_accessible(self_id, playlist, user, friends)

    return is_playlist_accessible_predicate


@v1.get(
    "/users/{user_id}/playlists",
    tags=[USERS, PLAYLISTS],
    summary="Fetches user playlists by the given ID.",
)
async def get_user_playlists(
    user_id: UUID,
    user_id_option: Optional[UUID] = Depends(optional_access_token_dependency),
    url: URL = Depends(request_url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserPlaylistsData:
    user = await database.query_user(user_id=user_id)

    if user is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    counted = await database.query_user_playlists(user_id=user_id)

    if counted is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    items, count = counted

    if user_id_option is None:
        items = iter(items).filter(is_playlist_public).list()

    else:
        friends = await are_friends(user_id_option, user_id)

        items = iter(items).filter(is_playlist_accessible_by(user_id_option, user, friends)).list()

    user_playlists = UserPlaylists(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return user_playlists.into_data()


INACCESSIBLE_FOLLOWERS = "the followers of the user with ID `{}` are inaccessible"


@v1.get(
    "/users/{user_id}/followers",
    tags=[USERS],
    summary="Fetches user followers by the given ID.",
)
async def get_user_followers(
    user_id: UUID,
    user_id_option: Optional[UUID] = Depends(optional_access_token_dependency),
    url: URL = Depends(request_url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserFollowersData:
    user = await database.query_user(user_id=user_id)

    if user is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    if user_id_option is None:
        accessible = is_user_public(user)

    else:
        friends = await are_friends(user_id_option, user_id)

        accessible = is_user_accessible(user_id_option, user, friends)

    if not accessible:
        raise Forbidden(INACCESSIBLE_FOLLOWERS.format(user_id))

    counted = await database.query_user_followers(user_id=user_id)

    if counted is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    items, count = counted

    user_followers = UserFollowers(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return user_followers.into_data()


INACCESSIBLE_FOLLOWING = "the following of the user with ID `{}` are inaccessible"


@v1.get(
    "/users/{user_id}/following",
    tags=[USERS],
    summary="Fetches user following by the given ID.",
)
async def get_user_following(
    user_id: UUID,
    user_id_option: Optional[UUID] = Depends(optional_access_token_dependency),
    url: URL = Depends(request_url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserFollowingData:
    user = await database.query_user(user_id=user_id)

    if user is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    if user_id_option is None:
        accessible = is_user_public(user)

    else:
        friends = await are_friends(user_id_option, user_id)

        accessible = is_user_accessible(user_id_option, user, friends)

    if not accessible:
        raise Forbidden(INACCESSIBLE_FOLLOWING.format(user_id))

    counted = await database.query_user_following(user_id=user_id)

    if counted is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    items, count = counted

    user_following = UserFollowing(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return user_following.into_data()


INACCESSIBLE_FRIENDS = "the friends of the user with ID `{}` are inaccessible"


@v1.get(
    "/users/{user_id}/friends",
    tags=[USERS],
    summary="Fetches user friends by the given ID.",
)
async def get_user_friends(
    user_id: UUID,
    user_id_option: Optional[UUID] = Depends(optional_access_token_dependency),
    url: URL = Depends(request_url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> UserFriendsData:
    user = await database.query_user(user_id=user_id)

    if user is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    if user_id_option is None:
        accessible = is_user_public(user)

    else:
        friends = await are_friends(user_id_option, user_id)

        accessible = is_user_accessible(user_id_option, user, friends)

    if not accessible:
        raise Forbidden(INACCESSIBLE_FRIENDS.format(user_id))

    counted = await database.query_user_friends(user_id=user_id)

    if counted is None:
        raise NotFound(CAN_NOT_FIND_USER.format(user_id))

    items, count = counted

    user_friends = UserFriends(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return user_friends.into_data()
