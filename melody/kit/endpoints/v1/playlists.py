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
from melody.kit.enums import EntityType, PrivacyType
from melody.kit.errors import Forbidden, NotFound, ValidationError
from melody.kit.models.base import BaseData
from melody.kit.models.pagination import Pagination
from melody.kit.models.playlist import (
    PlaylistData,
    PlaylistTracks,
    PlaylistTracksData,
)
from melody.kit.oauth2 import optional_token_dependency, token_dependency
from melody.kit.privacy import are_friends, is_playlist_accessible
from melody.kit.tags import IMAGES, LINKS, PLAYLISTS, TRACKS
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
    tags=[PLAYLISTS],
    summary="Creates a new playlist with the given name.",
)
async def create_playlist(
    name: str = Body(),
    description: Optional[str] = Body(default=None),
    privacy_type: PrivacyType = Body(default=PrivacyType.DEFAULT),
    self_id: UUID = Depends(token_dependency),
) -> BaseData:
    base = await database.insert_playlist(
        name=name, description=description, privacy_type=privacy_type, user_id=self_id
    )

    return base.into_data()


@v1.get(
    "/playlists/{playlist_id}",
    tags=[PLAYLISTS],
    summary="Fetches the playlist with the given ID.",
)
async def get_playlist(
    playlist_id: UUID,
    self_id_option: Optional[UUID] = Depends(optional_token_dependency),
) -> PlaylistData:
    playlist = await database.query_playlist(playlist_id=playlist_id)

    if playlist is None:
        raise NotFound(can_not_find_playlist(playlist_id))

    if self_id_option is None:
        accessible = playlist.privacy_type.is_public()

    else:
        self_id = self_id_option

        user_id = playlist.required_user.id

        friends = await are_friends(self_id, user_id)

        accessible = is_playlist_accessible(self_id, playlist, friends)

    if not accessible:
        raise Forbidden(inaccessible_playlist(playlist_id))

    return playlist.into_data()


@v1.put(
    "/playlists/{playlist_id}",
    tags=[PLAYLISTS],
    summary="Updates the playlist with the given ID.",
)
async def update_playlist(
    playlist_id: UUID,
    self_id: UUID = Depends(token_dependency),
    name: Optional[str] = Body(default=None),
    description: Optional[str] = Body(default=None),
    privacy_type: Optional[PrivacyType] = Body(default=None),
) -> None:
    if name is None and description is None and privacy_type is None:
        return  # there is nothing to update

    playlist = await database.query_playlist(playlist_id=playlist_id)

    if playlist is None:
        raise NotFound(can_not_find_playlist(playlist_id))

    if playlist.required_user.id != self_id:
        raise Forbidden(inaccessible_playlist(playlist_id))

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
async def delete_playlist(playlist_id: UUID, user_id: UUID = Depends(token_dependency)) -> None:
    playlist = await database.query_playlist(playlist_id=playlist_id)

    if playlist is None:
        raise NotFound(can_not_find_playlist(playlist_id))

    if playlist.required_user.id != user_id:
        raise Forbidden(inaccessible_playlist(playlist_id))

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
        raise NotFound(can_not_find_playlist_image(playlist_id))

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
    self_id: UUID = Depends(token_dependency),
) -> None:
    if not check_image_type(image):
        raise ValidationError(EXPECTED_IMAGE_TYPE)

    playlist = await database.query_playlist(playlist_id=playlist_id)

    if playlist is None:
        raise NotFound(can_not_find_playlist(playlist_id))

    if playlist.required_user.id != self_id:
        raise Forbidden(inaccessible_playlist(playlist_id))

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
    self_id_option: Optional[UUID] = Depends(optional_token_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
    url: URL = Depends(request_url_dependency),
) -> PlaylistTracksData:
    playlist = await database.query_playlist(playlist_id=playlist_id)

    if playlist is None:
        raise NotFound(can_not_find_playlist(playlist_id))

    if self_id_option is None:
        accessible = playlist.privacy_type.is_public()

    else:
        self_id = self_id_option

        user_id = playlist.required_user.id

        friends = await are_friends(self_id, user_id)

        accessible = is_playlist_accessible(self_id, playlist, friends)

    if not accessible:
        raise Forbidden(inaccessible_playlist(playlist_id))

    counted = await database.query_playlist_tracks(playlist_id=playlist_id)

    if counted is None:
        raise NotFound(can_not_find_playlist(playlist_id))

    items, count = counted

    playlist_tracks = PlaylistTracks(
        items, Pagination.paginate(url=url, count=count, offset=offset, limit=limit)
    )

    return playlist_tracks.into_data()
