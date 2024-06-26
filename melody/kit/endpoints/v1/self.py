from typing import List, Optional
from uuid import UUID

from async_extensions.paths import Path
from edgedb import QueryAssertionError
from fastapi import Body, Depends
from fastapi.responses import FileResponse
from typing_extensions import Annotated

from melody.kit.code import generate_code_for_uri
from melody.kit.core import config, database, v1
from melody.kit.dependencies.common import LimitDependency, OffsetDependency
from melody.kit.dependencies.images import ImageDependency
from melody.kit.dependencies.request_urls import RequestURLDependency
from melody.kit.enums import EntityType, Platform, PrivacyType, Tag
from melody.kit.errors.users import (
    UserFollowSelfForbidden,
    UserFollowSelfPlaylistsForbidden,
    UserImageNotFound,
    UserNotFound,
)
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
from melody.kit.tokens.dependencies import (
    FollowingReadTokenDependency,
    FollowingWriteTokenDependency,
    ImageReadTokenDependency,
    ImageWriteTokenDependency,
    LibraryReadTokenDependency,
    LibraryWriteTokenDependency,
    PlaylistsReadTokenDependency,
    SettingsReadTokenDependency,
    SettingsWriteTokenDependency,
    StreamsReadTokenDependency,
    UserBasedTokenDependency,
)
from melody.kit.uri import URI
from melody.shared.constants import WRITE_BINARY

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

UUIDListDependency = Annotated[List[UUID], Body()]


@v1.get(
    "/me",
    tags=[Tag.SELF],
    summary="Fetches self.",
)
async def get_self(context: UserBasedTokenDependency) -> UserData:
    self_id = context.user_id

    self = await database.query_user(user_id=self_id)

    if self is None:
        raise UserNotFound(self_id)

    return self.into_data()


@v1.get(
    "/me/link",
    tags=[Tag.SELF],
    summary="Fetches self link.",
)
async def get_self_link(context: UserBasedTokenDependency) -> FileResponse:
    uri = URI(type=EntityType.USER, id=context.user_id)

    path = await generate_code_for_uri(uri)

    return FileResponse(path)


@v1.get(
    "/me/image",
    tags=[Tag.SELF],
    summary="Fetches self image.",
)
async def get_self_image(context: ImageReadTokenDependency) -> FileResponse:
    self_id = context.user_id

    uri = URI(type=EntityType.USER, id=self_id)

    path = Path(config.image.directory_path / uri.image_name)

    if not await path.exists():
        raise UserImageNotFound(self_id)

    return FileResponse(path)


@v1.put(
    "/me/image",
    tags=[Tag.SELF],
    summary="Changes self image.",
)
async def change_self_image(context: ImageWriteTokenDependency, data: ImageDependency) -> None:
    uri = URI(type=EntityType.USER, id=context.user_id)

    path = Path(config.image.directory_path / uri.image_name)

    async with await path.open(WRITE_BINARY) as file:
        await file.write(data)


@v1.delete(
    "/me/image",
    tags=[Tag.SELF],
    summary="Removes self image.",
)
async def remove_self_image(context: ImageWriteTokenDependency) -> None:
    self_id = context.user_id

    uri = URI(type=EntityType.USER, id=self_id)

    path = Path(config.image.directory_path / uri.image_name)

    await path.unlink(missing_ok=True)


@v1.get(
    "/me/tracks",
    tags=[Tag.SELF],
    summary="Fetches saved tracks.",
)
async def get_self_tracks(
    context: LibraryReadTokenDependency,
    request_url: RequestURLDependency,
    offset: OffsetDependency = config.offset.default,
    limit: LimitDependency = config.limit.default,
) -> UserTracksData:
    self_id = context.user_id

    counted = await database.query_user_tracks(user_id=self_id, offset=offset, limit=limit)

    if counted is None:
        raise UserNotFound(self_id)

    items, count = counted

    self_tracks = UserTracks(
        items, Pagination.paginate(url=request_url, offset=offset, limit=limit, count=count)
    )

    return self_tracks.into_data()


@v1.put(
    "/me/tracks",
    tags=[Tag.SELF],
    summary="Saves tracks.",
)
async def save_self_tracks(context: LibraryWriteTokenDependency, ids: UUIDListDependency) -> None:
    await database.save_user_tracks(user_id=context.user_id, ids=ids)


@v1.delete(
    "/me/tracks",
    tags=[Tag.SELF],
    summary="Removes saved tracks.",
)
async def remove_self_tracks(context: LibraryWriteTokenDependency, ids: UUIDListDependency) -> None:
    await database.remove_user_tracks(user_id=context.user_id, ids=ids)


@v1.get(
    "/me/artists",
    tags=[Tag.SELF],
    summary="Fetches saved artists.",
)
async def get_self_artists(
    context: LibraryReadTokenDependency,
    request_url: RequestURLDependency,
    offset: OffsetDependency = config.offset.default,
    limit: LimitDependency = config.limit.default,
) -> UserArtistsData:
    self_id = context.user_id

    counted = await database.query_user_artists(user_id=self_id, offset=offset, limit=limit)

    if counted is None:
        raise UserNotFound(self_id)

    items, count = counted

    self_artists = UserArtists(
        items, Pagination.paginate(url=request_url, offset=offset, limit=limit, count=count)
    )

    return self_artists.into_data()


@v1.put(
    "/me/artists",
    tags=[Tag.SELF],
    summary="Saves artists.",
)
async def save_self_artists(context: LibraryWriteTokenDependency, ids: UUIDListDependency) -> None:
    await database.save_user_artists(user_id=context.user_id, ids=ids)


@v1.delete(
    "/me/artists",
    tags=[Tag.SELF],
    summary="Removes saved artists.",
)
async def remove_self_artists(
    context: LibraryWriteTokenDependency, ids: UUIDListDependency
) -> None:
    await database.remove_user_artists(user_id=context.user_id, ids=ids)


@v1.get(
    "/me/albums",
    tags=[Tag.SELF],
    summary="Fetches saved albums.",
)
async def get_self_albums(
    context: LibraryReadTokenDependency,
    request_url: RequestURLDependency,
    offset: OffsetDependency = config.offset.default,
    limit: LimitDependency = config.limit.default,
) -> UserAlbumsData:
    self_id = context.user_id

    counted = await database.query_user_albums(user_id=self_id, offset=offset, limit=limit)

    if counted is None:
        raise UserNotFound(self_id)

    items, count = counted

    self_albums = UserAlbums(
        items, Pagination.paginate(url=request_url, offset=offset, limit=limit, count=count)
    )

    return self_albums.into_data()


@v1.put(
    "/me/albums",
    tags=[Tag.SELF],
    summary="Saves albums.",
)
async def save_self_albums(context: LibraryWriteTokenDependency, ids: UUIDListDependency) -> None:
    await database.save_user_albums(user_id=context.user_id, ids=ids)


@v1.delete(
    "/me/albums",
    tags=[Tag.SELF],
    summary="Removes saved albums.",
)
async def remove_self_albums(context: LibraryWriteTokenDependency, ids: UUIDListDependency) -> None:
    await database.remove_user_albums(user_id=context.user_id, ids=ids)


@v1.get(
    "/me/playlists",
    tags=[Tag.SELF],
    summary="Fetches playlists.",
)
async def get_self_playlists(
    context: PlaylistsReadTokenDependency,
    request_url: RequestURLDependency,
    offset: OffsetDependency = config.offset.default,
    limit: LimitDependency = config.limit.default,
) -> UserPlaylistsData:
    self_id = context.user_id

    counted = await database.query_user_playlists(user_id=self_id, offset=offset, limit=limit)

    if counted is None:
        raise UserNotFound(self_id)

    items, count = counted

    self_playlists = UserPlaylists(
        items, Pagination.paginate(url=request_url, offset=offset, limit=limit, count=count)
    )

    return self_playlists.into_data()


@v1.get(
    "/me/streams",
    tags=[Tag.SELF],
    summary="Fetches streams.",
)
async def get_self_streams(
    context: StreamsReadTokenDependency,
    request_url: RequestURLDependency,
    offset: OffsetDependency = config.offset.default,
    limit: LimitDependency = config.limit.default,
) -> UserStreamsData:
    self_id = context.user_id

    counted = await database.query_user_streams(user_id=self_id, offset=offset, limit=limit)

    if counted is None:
        raise UserNotFound(self_id)

    items, count = counted

    self_streams = UserStreams(
        items, Pagination.paginate(url=request_url, offset=offset, limit=limit, count=count)
    )

    return self_streams.into_data()


@v1.get(
    "/me/friends",
    tags=[Tag.SELF],
    summary="Fetches friends.",
)
async def get_self_friends(
    context: FollowingReadTokenDependency,
    request_url: RequestURLDependency,
    offset: OffsetDependency = config.offset.default,
    limit: LimitDependency = config.limit.default,
) -> UserFriendsData:
    self_id = context.user_id

    counted = await database.query_user_friends(user_id=self_id, offset=offset, limit=limit)

    if counted is None:
        raise UserNotFound(self_id)

    items, count = counted

    self_friends = UserFriends(
        items, Pagination.paginate(url=request_url, offset=offset, limit=limit, count=count)
    )

    return self_friends.into_data()


@v1.get(
    "/me/followers",
    tags=[Tag.SELF],
    summary="Fetches followers.",
)
async def get_self_followers(
    context: FollowingReadTokenDependency,
    request_url: RequestURLDependency,
    offset: OffsetDependency = config.offset.default,
    limit: LimitDependency = config.limit.default,
) -> UserFollowersData:
    self_id = context.user_id

    counted = await database.query_user_followers(user_id=self_id, offset=offset, limit=limit)

    if counted is None:
        raise UserNotFound(self_id)

    items, count = counted

    self_followers = UserFollowers(
        items, Pagination.paginate(url=request_url, offset=offset, limit=limit, count=count)
    )

    return self_followers.into_data()


@v1.get(
    "/me/following",
    tags=[Tag.SELF],
    summary="Fetches following.",
)
async def get_self_following(
    context: FollowingReadTokenDependency,
    request_url: RequestURLDependency,
    offset: OffsetDependency = config.offset.default,
    limit: LimitDependency = config.limit.default,
) -> UserFollowingData:
    self_id = context.user_id

    counted = await database.query_user_following(user_id=self_id, offset=offset, limit=limit)

    if counted is None:
        raise UserNotFound(self_id)

    items, count = counted

    self_following = UserFollowing(
        items, Pagination.paginate(url=request_url, offset=offset, limit=limit, count=count)
    )

    return self_following.into_data()


@v1.put(
    "/me/following",
    tags=[Tag.SELF],
    summary="Follows users.",
)
async def add_self_following(
    context: FollowingWriteTokenDependency, ids: UUIDListDependency
) -> None:
    self_id = context.user_id

    try:
        await database.add_user_following(user_id=self_id, ids=ids)

    except QueryAssertionError:
        raise UserFollowSelfForbidden(self_id) from None


@v1.delete(
    "/me/following",
    tags=[Tag.SELF],
    summary="Unfollows users.",
)
async def remove_self_following(
    context: FollowingWriteTokenDependency, ids: UUIDListDependency
) -> None:
    await database.remove_user_following(user_id=context.user_id, ids=ids)


@v1.get(
    "/me/playlists/followed",
    tags=[Tag.SELF],
    summary="Fetches followed playlists.",
)
async def get_self_followed_playlists(
    context: LibraryReadTokenDependency,
    request_url: RequestURLDependency,
    offset: OffsetDependency = config.offset.default,
    limit: LimitDependency = config.limit.default,
) -> UserFollowedPlaylistsData:
    self_id = context.user_id

    counted = await database.query_user_followed_playlists(
        user_id=self_id, offset=offset, limit=limit
    )

    if counted is None:
        raise UserNotFound(self_id)

    items, count = counted

    self_followed_playlists = UserFollowedPlaylists(
        items, Pagination.paginate(url=request_url, offset=offset, limit=limit, count=count)
    )

    return self_followed_playlists.into_data()


@v1.put(
    "/me/playlists/followed",
    tags=[Tag.SELF],
    summary="Follows playlists.",
)
async def add_self_followed_playlists(
    context: LibraryWriteTokenDependency, ids: UUIDListDependency
) -> None:
    self_id = context.user_id

    try:
        await database.add_user_followed_playlists(user_id=self_id, ids=ids)

    except QueryAssertionError:
        raise UserFollowSelfPlaylistsForbidden(self_id) from None


@v1.delete(
    "/me/playlists/followed",
    tags=[Tag.SELF],
    summary="Unfollows playlists.",
)
async def remove_self_followed_playlists(
    context: LibraryWriteTokenDependency, ids: UUIDListDependency
) -> None:
    await database.remove_user_followed_playlists(user_id=context.user_id, ids=ids)


@v1.get(
    "/me/settings",
    tags=[Tag.SELF],
    summary="Fetches self settings.",
)
async def get_self_settings(context: SettingsReadTokenDependency) -> UserSettingsData:
    self_id = context.user_id

    self_settings = await database.query_user_settings(user_id=self_id)

    if self_settings is None:
        raise UserNotFound(self_id)

    return self_settings.into_data()


OptionalNameDependency = Annotated[Optional[str], Body()]
OptionalExplicitDependency = Annotated[Optional[bool], Body()]
OptionalAutoplayDependency = Annotated[Optional[bool], Body()]
OptionalPlatformDependency = Annotated[Optional[Platform], Body()]
OptionalPrivacyTypeDependency = Annotated[Optional[PrivacyType], Body()]


class UpdateSelfSettingsPayload:
    def __init__(
        self,
        name: OptionalNameDependency = None,
        explicit: OptionalExplicitDependency = None,
        autoplay: OptionalAutoplayDependency = None,
        platform: OptionalPlatformDependency = None,
        privacy_type: OptionalPrivacyTypeDependency = None,
    ) -> None:
        self.name = name
        self.explicit = explicit
        self.autoplay = autoplay
        self.platform = platform
        self.privacy_type = privacy_type


UpdateSelfSettingsPayloadDependency = Annotated[UpdateSelfSettingsPayload, Depends()]


@v1.put(
    "/me/settings",
    tags=[Tag.SELF],
    summary="Changes self settings.",
)
async def update_self_settings(
    context: SettingsWriteTokenDependency,
    payload: UpdateSelfSettingsPayloadDependency,
) -> None:
    self_id = context.user_id

    name = payload.name
    explicit = payload.explicit
    autoplay = payload.autoplay
    platform = payload.platform
    privacy_type = payload.privacy_type

    if (
        name is None
        and explicit is None
        and autoplay is None
        and platform is None
        and privacy_type is None
    ):
        return  # there is nothing to update

    settings = await database.query_user_settings(user_id=self_id)

    if settings is None:
        raise UserNotFound(self_id)

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
        user_id=self_id,
        name=name,
        explicit=explicit,
        autoplay=autoplay,
        platform=platform,
        privacy_type=privacy_type,
    )
