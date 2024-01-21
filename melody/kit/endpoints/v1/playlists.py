from typing import Optional
from uuid import UUID

from fastapi import Body, Depends, File, Query, UploadFile
from fastapi.responses import FileResponse
from yarl import URL

from melody.kit.constants import (
    DEFAULT_LIMIT,
    DEFAULT_OFFSET,
    MAX_LIMIT,
    MIN_LIMIT,
    MIN_OFFSET,
)
from melody.kit.core import config, database, v1
from melody.kit.dependencies import (
    access_token_dependency,
    optional_access_token_dependency,
    url_dependency,
)
from melody.kit.enums import EntityType, PrivacyType
from melody.kit.errors import Forbidden, NotFound, ValidationError
from melody.kit.link import generate_code_for_uri
from melody.kit.models.base import BaseData
from melody.kit.models.pagination import Pagination
from melody.kit.models.playlist import (
    Playlist,
    PlaylistData,
    PlaylistTracks,
    PlaylistTracksData,
)
from melody.kit.tags import IMAGES, LINKS, PLAYLISTS, TRACKS
from melody.kit.uri import URI
from melody.shared.constants import EMPTY, IMAGE_TYPE
from melody.shared.image import check_image_type, validate_and_save_image

__all__ = (
    "create_playlist",
    "get_playlist",
    "update_playlist",
    "delete_playlist",
    "get_playlist_link",
    "get_playlist_image",
    "change_playlist_image",
    "get_playlist_tracks",
)

CAN_NOT_FIND_PLAYLIST = "can not find the playlist with ID `{}`"
CAN_NOT_FIND_PLAYLIST_IMAGE = "can not find the image for the playlist with ID `{}`"
INACCESSIBLE_PLAYLIST = "the playlist with ID `{}` is inaccessible"


async def check_accessible(playlist: Playlist, user_id_option: Optional[UUID]) -> bool:
    playlist_user = playlist.user
    playlist_user_id = playlist_user.id

    if user_id_option is not None:
        if user_id_option == playlist_user_id:
            return True

    playlist_privacy_type = playlist.privacy_type
    playlist_user_privacy_type = playlist_user.privacy_type

    private = playlist_privacy_type.is_private() or playlist_user_privacy_type.is_private()
    friends = playlist_privacy_type.is_friends() or playlist_user_privacy_type.is_friends()

    if private:
        return False

    if friends:
        return user_id_option is not None and await database.check_user_friends(
            user_id=playlist_user_id, target_id=user_id_option
        )

    return True


@v1.post(
    "/playlists",
    tags=[PLAYLISTS],
    summary="Creates a new playlist with the given name.",
)
async def create_playlist(
    name: str = Body(),
    description: str = Body(default=EMPTY),
    privacy_type: PrivacyType = Body(default=PrivacyType.DEFAULT),
    user_id: UUID = Depends(access_token_dependency),
) -> BaseData:
    base = await database.insert_playlist(
        name=name, description=description, privacy_type=privacy_type, user_id=user_id
    )

    return base.into_data()


@v1.get(
    "/playlists/{playlist_id}",
    tags=[PLAYLISTS],
    summary="Fetches the playlist with the given ID.",
)
async def get_playlist(
    playlist_id: UUID,
    user_id_option: Optional[UUID] = Depends(optional_access_token_dependency),
) -> PlaylistData:
    playlist = await database.query_playlist(playlist_id=playlist_id)

    if playlist is None:
        raise NotFound(CAN_NOT_FIND_PLAYLIST.format(playlist_id))

    if await check_accessible(playlist, user_id_option):
        return playlist.into_data()

    raise Forbidden(INACCESSIBLE_PLAYLIST.format(playlist_id))


@v1.put(
    "/playlists/{playlist_id}",
    tags=[PLAYLISTS],
    summary="Updates the playlist with the given ID.",
)
async def update_playlist(
    playlist_id: UUID,
    user_id: UUID = Depends(access_token_dependency),
    name: Optional[str] = Body(default=None),
    description: Optional[str] = Body(default=None),
    privacy_type: Optional[PrivacyType] = Body(default=None),
) -> None:
    if name is None and description is None and privacy_type is None:
        return  # there is nothing to update

    playlist = await database.query_playlist(playlist_id=playlist_id)

    if playlist is None:
        raise NotFound(CAN_NOT_FIND_PLAYLIST.format(playlist_id))

    if playlist.user.id != user_id:
        raise Forbidden(INACCESSIBLE_PLAYLIST.format(playlist_id))

    if name is None:
        name = playlist.name

    if description is None:
        description = playlist.description

    if privacy_type is None:
        privacy_type = playlist.privacy_type

    await database.update_playlist(
        playlist_id=playlist_id,
        name=name,
        description=description,
        privacy_type=privacy_type,
    )


@v1.delete(
    "/playlists/{playlist_id}",
    tags=[PLAYLISTS],
    summary="Deletes the playlist with the given ID.",
)
async def delete_playlist(
    playlist_id: UUID, user_id: UUID = Depends(access_token_dependency)
) -> None:
    playlist = await database.query_playlist(playlist_id=playlist_id)

    if playlist is None:
        raise NotFound(CAN_NOT_FIND_PLAYLIST.format(playlist_id))

    if playlist.user.id != user_id:
        raise Forbidden(INACCESSIBLE_PLAYLIST.format(playlist_id))

    await database.delete_playlist(playlist_id=playlist_id)


@v1.get(
    "/playlists/{playlist_id}/link",
    tags=[PLAYLISTS, LINKS],
    summary="Fetches the playlist link with the given ID.",
)
async def get_playlist_link(playlist_id: UUID) -> FileResponse:
    uri = URI(type=EntityType.PLAYLIST, id=playlist_id)

    path = await generate_code_for_uri(uri)

    return FileResponse(path)


@v1.get(
    "/playlists/{playlist_id}/image",
    tags=[PLAYLISTS, IMAGES],
    summary="Fetches the playlist image with the given ID.",
)
async def get_playlist_image(playlist_id: UUID) -> FileResponse:
    uri = URI(type=EntityType.PLAYLIST, id=playlist_id)

    path = config.images / uri.image_name

    if not path.exists():
        raise NotFound(CAN_NOT_FIND_PLAYLIST_IMAGE.format(playlist_id))

    return FileResponse(path)


EXPECTED_IMAGE_TYPE = f"expected `{IMAGE_TYPE}` image type"
EXPECTED_SQUARE_IMAGE = "expected square image"


@v1.put(
    "/playlists/{playlist_id}/image",
    tags=[PLAYLISTS, IMAGES],
    summary="Changes the playlist image with the given ID.",
)
async def change_playlist_image(
    playlist_id: UUID,
    image: UploadFile = File(),
    user_id: UUID = Depends(access_token_dependency),
) -> None:
    if not check_image_type(image):
        raise ValidationError(EXPECTED_IMAGE_TYPE)

    playlist = await database.query_playlist(playlist_id=playlist_id)

    if playlist is None:
        raise NotFound(CAN_NOT_FIND_PLAYLIST.format(playlist_id))

    if playlist.user.id != user_id:
        raise Forbidden(INACCESSIBLE_PLAYLIST.format(playlist_id))

    path = config.images / playlist.uri.image_name

    if not await validate_and_save_image(image, path):
        raise ValidationError(EXPECTED_SQUARE_IMAGE)


@v1.get(
    "/playlists/{playlist_id}/tracks",
    tags=[PLAYLISTS, TRACKS],
    summary="Fetches playlist tracks with the given ID.",
)
async def get_playlist_tracks(
    playlist_id: UUID,
    user_id_option: Optional[UUID] = Depends(optional_access_token_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
    url: URL = Depends(url_dependency),
) -> PlaylistTracksData:
    playlist = await database.query_playlist(playlist_id=playlist_id)

    if playlist is None:
        raise NotFound(CAN_NOT_FIND_PLAYLIST.format(playlist_id))

    if await check_accessible(playlist, user_id_option):
        counted = await database.query_playlist_tracks(playlist_id=playlist_id)

        if counted is None:
            raise NotFound(CAN_NOT_FIND_PLAYLIST.format(playlist_id))

        items, count = counted

        playlist_tracks = PlaylistTracks(
            items, Pagination.paginate(url=url, count=count, offset=offset, limit=limit)
        )

        return playlist_tracks.into_data()

    raise Forbidden(INACCESSIBLE_PLAYLIST.format(playlist_id))
