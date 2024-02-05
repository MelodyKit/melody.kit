from typing import Optional
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
from melody.kit.dependencies import request_url_dependency
from melody.kit.enums import EntityType, PrivacyType, Tag
from melody.kit.errors import NotFound, ValidationError
from melody.kit.models.base import BaseData
from melody.kit.models.pagination import Pagination
from melody.kit.models.playlist import PlaylistData, PlaylistTracks, PlaylistTracksData
from melody.kit.oauth2 import optional_token_dependency, token_dependency
from melody.kit.privacy import (
    check_playlist_accessible_dependency,
    check_playlist_changeable_dependency,
)
from melody.kit.uri import URI
from melody.shared.constants import IMAGE_TYPE
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
can_not_find_playlist = CAN_NOT_FIND_PLAYLIST.format

CAN_NOT_FIND_PLAYLIST_IMAGE = "can not find the image for the playlist with ID `{}`"
can_not_find_playlist_image = CAN_NOT_FIND_PLAYLIST_IMAGE.format

INACCESSIBLE_PLAYLIST = "the playlist with ID `{}` is inaccessible"
inaccessible_playlist = INACCESSIBLE_PLAYLIST.format


@v1.post(
    "/playlists",
    tags=[Tag.PLAYLISTS],
    summary="Creates a new playlist.",
)
async def create_playlist(
    name: str = Body(),
    description: Optional[str] = Body(default=None),
    privacy_type: PrivacyType = Body(default=PrivacyType.DEFAULT),
    self_id: UUID = Depends(token_dependency),
) -> BaseData:
    base = await database.insert_playlist(
        name=name, description=description, privacy_type=privacy_type, owner_id=self_id
    )

    return base.into_data()


@v1.get(
    "/playlists/{playlist_id}",
    tags=[Tag.PLAYLISTS],
    summary="Fetches the playlist.",
    dependencies=[Depends(check_playlist_accessible_dependency)],
)
async def get_playlist(
    playlist_id: UUID,
    self_id: Optional[UUID] = Depends(optional_token_dependency),
) -> PlaylistData:
    playlist = await database.query_playlist(playlist_id=playlist_id)

    if playlist is None:
        raise NotFound(can_not_find_playlist(playlist_id))

    return playlist.into_data()


@v1.put(
    "/playlists/{playlist_id}",
    tags=[Tag.PLAYLISTS],
    summary="Updates the playlist.",
    dependencies=[Depends(check_playlist_changeable_dependency)],
)
async def update_playlist(
    playlist_id: UUID,
    name: Optional[str] = Body(default=None),
    description: Optional[str] = Body(default=None),
    privacy_type: Optional[PrivacyType] = Body(default=None),
) -> None:
    if name is None and description is None and privacy_type is None:
        return  # there is nothing to update

    playlist = await database.query_playlist(playlist_id=playlist_id)

    if playlist is None:
        raise NotFound(can_not_find_playlist(playlist_id))

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
    tags=[Tag.PLAYLISTS],
    summary="Deletes the playlist.",
    dependencies=[Depends(check_playlist_changeable_dependency)],
)
async def delete_playlist(playlist_id: UUID, user_id: UUID = Depends(token_dependency)) -> None:
    playlist = await database.query_playlist(playlist_id=playlist_id)

    if playlist is None:
        raise NotFound(can_not_find_playlist(playlist_id))

    await database.delete_playlist(playlist_id=playlist_id)


@v1.get(
    "/playlists/{playlist_id}/link",
    tags=[Tag.PLAYLISTS],
    summary="Fetches the playlist's link.",
)
async def get_playlist_link(playlist_id: UUID) -> FileResponse:
    uri = URI(type=EntityType.PLAYLIST, id=playlist_id)

    path = await generate_code_for_uri(uri)

    return FileResponse(path)


@v1.get(
    "/playlists/{playlist_id}/image",
    tags=[Tag.PLAYLISTS],
    summary="Fetches the playlist's image.",
    dependencies=[Depends(check_playlist_accessible_dependency)],
)
async def get_playlist_image(playlist_id: UUID) -> FileResponse:
    uri = URI(type=EntityType.PLAYLIST, id=playlist_id)

    path = config.images / uri.image_name

    if not path.exists():
        raise NotFound(can_not_find_playlist_image(playlist_id))

    return FileResponse(path)


EXPECTED_IMAGE_TYPE = f"expected `{IMAGE_TYPE}` image type"
EXPECTED_SQUARE_IMAGE = "expected square image"


@v1.put(
    "/playlists/{playlist_id}/image",
    tags=[Tag.PLAYLISTS],
    summary="Changes the playlist's image.",
    dependencies=[Depends(check_playlist_changeable_dependency)],
)
async def change_playlist_image(playlist_id: UUID, image: UploadFile = File()) -> None:
    if not check_image_type(image):
        raise ValidationError(EXPECTED_IMAGE_TYPE)

    uri = URI(type=EntityType.PLAYLIST, id=playlist_id)

    path = config.images / uri.image_name

    if not await validate_and_save_image(image, path):
        raise ValidationError(EXPECTED_SQUARE_IMAGE)


@v1.get(
    "/playlists/{playlist_id}/tracks",
    tags=[Tag.PLAYLISTS],
    summary="Fetches the playlist's tracks.",
    dependencies=[Depends(check_playlist_accessible_dependency)],
)
async def get_playlist_tracks(
    playlist_id: UUID,
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
    url: URL = Depends(request_url_dependency),
) -> PlaylistTracksData:
    counted = await database.query_playlist_tracks(
        playlist_id=playlist_id, offset=offset, limit=limit
    )

    if counted is None:
        raise NotFound(can_not_find_playlist(playlist_id))

    items, count = counted

    playlist_tracks = PlaylistTracks(
        items, Pagination.paginate(url=url, count=count, offset=offset, limit=limit)
    )

    return playlist_tracks.into_data()
