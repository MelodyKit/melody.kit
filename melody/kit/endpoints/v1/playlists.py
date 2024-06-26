from typing import Optional
from uuid import UUID

from async_extensions.paths import Path
from fastapi import Body, Depends
from fastapi.responses import FileResponse
from typing_extensions import Annotated

from melody.kit.code import generate_code_for_uri
from melody.kit.core import config, database, v1
from melody.kit.dependencies.common import LimitDependency, OffsetDependency
from melody.kit.dependencies.images import ImageDependency
from melody.kit.dependencies.request_urls import RequestURLDependency
from melody.kit.enums import EntityType, PrivacyType, Tag
from melody.kit.errors.playlists import PlaylistImageNotFound, PlaylistNotFound
from melody.kit.models.base import BaseData
from melody.kit.models.pagination import Pagination
from melody.kit.models.playlist import PlaylistData, PlaylistTracks, PlaylistTracksData
from melody.kit.tokens.dependencies import PlaylistsWriteTokenDependency, token_dependency
from melody.kit.uri import URI
from melody.shared.constants import IMAGE_TYPE, WRITE_BINARY

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
)
async def get_playlist(playlist_id: UUID) -> PlaylistData:
    playlist = await database.query_playlist(playlist_id=playlist_id)

    if playlist is None:
        raise PlaylistNotFound(playlist_id)

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
        raise PlaylistNotFound(playlist_id)

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
)
async def delete_playlist(playlist_id: UUID) -> None:
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
)
async def get_playlist_image(playlist_id: UUID) -> FileResponse:
    uri = URI(type=EntityType.PLAYLIST, id=playlist_id)

    path = Path(config.image.directory_path / uri.image_name)

    if not await path.exists():
        raise PlaylistImageNotFound(playlist_id)

    return FileResponse(path)


EXPECTED_IMAGE_TYPE = f"expected `{IMAGE_TYPE}` image type"
EXPECTED_SQUARE_IMAGE = "expected square image"


@v1.put(
    "/playlists/{playlist_id}/image",
    tags=[Tag.PLAYLISTS],
    summary="Changes the playlist's image.",
)
async def change_playlist_image(playlist_id: UUID, data: ImageDependency) -> None:
    uri = URI(type=EntityType.PLAYLIST, id=playlist_id)

    path = Path(config.image.directory_path / uri.image_name)

    async with await path.open(WRITE_BINARY) as file:
        await file.write(data)


@v1.delete(
    "/playlists/{playlist_id}/image",
    tags=[Tag.PLAYLISTS],
    summary="Removes the playlist's image.",
)
async def remove_playlist_image(playlist_id: UUID) -> None:
    uri = URI(type=EntityType.PLAYLIST, id=playlist_id)

    path = Path(config.image.directory_path / uri.image_name)

    await path.unlink(missing_ok=True)


@v1.get(
    "/playlists/{playlist_id}/tracks",
    tags=[Tag.PLAYLISTS],
    summary="Fetches the playlist's tracks.",
)
async def get_playlist_tracks(
    playlist_id: UUID,
    request_url: RequestURLDependency,
    offset: OffsetDependency = config.offset.default,
    limit: LimitDependency = config.limit.default,
) -> PlaylistTracksData:
    counted = await database.query_playlist_tracks(
        playlist_id=playlist_id, offset=offset, limit=limit
    )

    if counted is None:
        raise PlaylistNotFound(playlist_id)

    items, count = counted

    playlist_tracks = PlaylistTracks(
        items, Pagination.paginate(url=request_url, count=count, offset=offset, limit=limit)
    )

    return playlist_tracks.into_data()
