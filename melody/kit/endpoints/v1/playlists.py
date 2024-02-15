from typing import Optional
from typing_extensions import Annotated
from uuid import UUID

from fastapi import Body, Depends
from fastapi.responses import FileResponse

from melody.kit.code import generate_code_for_uri
from melody.kit.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from melody.kit.core import config, database, v1
from melody.kit.dependencies import (
    FileDependency,
    LimitDependency,
    OffsetDependency,
    RequestURLDependency,
)
from melody.kit.enums import EntityType, PrivacyType, Tag
from melody.kit.errors import NotFound, ValidationError
from melody.kit.models.base import BaseData
from melody.kit.models.pagination import Pagination
from melody.kit.models.playlist import PlaylistData, PlaylistTracks, PlaylistTracksData
from melody.kit.oauth2 import PlaylistsWriteTokenDependency, token_dependency
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
    "remove_playlist_image",
    "get_playlist_tracks",
)

CAN_NOT_FIND_PLAYLIST = "can not find the playlist with ID `{}`"
can_not_find_playlist = CAN_NOT_FIND_PLAYLIST.format

CAN_NOT_FIND_PLAYLIST_IMAGE = "can not find the image for the playlist with ID `{}`"
can_not_find_playlist_image = CAN_NOT_FIND_PLAYLIST_IMAGE.format

INACCESSIBLE_PLAYLIST = "the playlist with ID `{}` is inaccessible"
inaccessible_playlist = INACCESSIBLE_PLAYLIST.format


NameDependency = Annotated[str, Body()]
OptionalDescriptionDependency = Annotated[Optional[str], Body()]
PrivacyTypeDependency = Annotated[PrivacyType, Body()]


class CreatePlaylistPayload:
    def __init__(
        self,
        name: NameDependency,
        description: OptionalDescriptionDependency = None,
        privacy_type: PrivacyTypeDependency = PrivacyType.DEFAULT,
    ) -> None:
        self.name = name
        self.description = description
        self.privacy_type = privacy_type


CreatePlaylistPayloadDependency = Annotated[CreatePlaylistPayload, Depends()]


@v1.post(
    "/playlists",
    tags=[Tag.PLAYLISTS],
    summary="Creates a new playlist.",
)
async def create_playlist(
    payload: CreatePlaylistPayloadDependency,
    context: PlaylistsWriteTokenDependency,
) -> BaseData:
    base = await database.insert_playlist(
        name=payload.name,
        description=payload.description,
        privacy_type=payload.privacy_type,
        owner_id=context.user_id,
    )

    return base.into_data()


@v1.get(
    "/playlists/{playlist_id}",
    tags=[Tag.PLAYLISTS],
    summary="Fetches the playlist.",
    dependencies=[Depends(check_playlist_accessible_dependency)],
)
async def get_playlist(playlist_id: UUID) -> PlaylistData:
    playlist = await database.query_playlist(playlist_id=playlist_id)

    if playlist is None:
        raise NotFound(can_not_find_playlist(playlist_id))

    return playlist.into_data()


OptionalNameDependency = Annotated[Optional[str], Body()]
OptionalPrivacyTypeDependency = Annotated[Optional[PrivacyType], Body()]


class UpdatePlaylistPayload:
    def __init__(
        self,
        name: OptionalNameDependency = None,
        description: OptionalDescriptionDependency = None,
        privacy_type: OptionalPrivacyTypeDependency = None,
    ) -> None:
        self.name = name
        self.description = description
        self.privacy_type = privacy_type


UpdatePlaylistPayloadDependency = Annotated[UpdatePlaylistPayload, Depends()]


@v1.put(
    "/playlists/{playlist_id}",
    tags=[Tag.PLAYLISTS],
    summary="Updates the playlist.",
    dependencies=[Depends(check_playlist_changeable_dependency)],
)
async def update_playlist(
    playlist_id: UUID,
    payload: UpdatePlaylistPayloadDependency,
) -> None:
    name = payload.name
    description = payload.description
    privacy_type = payload.privacy_type

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
async def delete_playlist(playlist_id: UUID) -> None:
    playlist = await database.query_playlist(playlist_id=playlist_id)

    if playlist is None:
        raise NotFound(can_not_find_playlist(playlist_id))

    await database.delete_playlist(playlist_id=playlist_id)


@v1.get(
    "/playlists/{playlist_id}/link",
    tags=[Tag.PLAYLISTS],
    summary="Fetches the playlist's link.",
    dependencies=[Depends(token_dependency)],
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
async def change_playlist_image(playlist_id: UUID, image: FileDependency) -> None:
    if not check_image_type(image):
        raise ValidationError(EXPECTED_IMAGE_TYPE)

    uri = URI(type=EntityType.PLAYLIST, id=playlist_id)

    path = config.images / uri.image_name

    if not await validate_and_save_image(image, path):
        raise ValidationError(EXPECTED_SQUARE_IMAGE)


@v1.delete(
    "/playlists/{playlist_id}/image",
    tags=[Tag.PLAYLISTS],
    summary="Removes the playlist's image.",
    dependencies=[Depends(check_playlist_changeable_dependency)],
)
async def remove_playlist_image(playlist_id: UUID) -> None:
    uri = URI(type=EntityType.PLAYLIST, id=playlist_id)

    path = config.images / uri.image_name

    path.unlink(missing_ok=True)


@v1.get(
    "/playlists/{playlist_id}/tracks",
    tags=[Tag.PLAYLISTS],
    summary="Fetches the playlist's tracks.",
    dependencies=[Depends(check_playlist_accessible_dependency)],
)
async def get_playlist_tracks(
    playlist_id: UUID,
    request_url: RequestURLDependency,
    offset: OffsetDependency = DEFAULT_OFFSET,
    limit: LimitDependency = DEFAULT_LIMIT,
) -> PlaylistTracksData:
    counted = await database.query_playlist_tracks(
        playlist_id=playlist_id, offset=offset, limit=limit
    )

    if counted is None:
        raise NotFound(can_not_find_playlist(playlist_id))

    items, count = counted

    playlist_tracks = PlaylistTracks(
        items, Pagination.paginate(url=request_url, count=count, offset=offset, limit=limit)
    )

    return playlist_tracks.into_data()
