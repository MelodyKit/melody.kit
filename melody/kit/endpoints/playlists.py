from typing import Optional
from uuid import UUID

from async_extensions.file import open_file
from fastapi import Body, Depends, File, UploadFile
from fastapi.responses import FileResponse
from iters import iter

from melody.kit.core import config, database, v1
from melody.kit.dependencies import optional_token_dependency, token_dependency
from melody.kit.enums import EntityType, PrivacyType
from melody.kit.errors import Forbidden, NotFound, ValidationError
from melody.kit.models.playlist import (
    Playlist,
    PlaylistData,
    PlaylistTracksData,
    playlist_into_data,
)
from melody.kit.models.track import position_track_into_data
from melody.kit.tags import IMAGES, LINKS, PLAYLISTS, TRACKS
from melody.kit.uri import URI
from melody.shared.constants import IMAGE_CONTENT_TYPE, IMAGE_TYPE, WRITE_BINARY

__all__ = ("get_playlist", "get_playlist_link", "get_playlist_tracks")

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
            playlist_user_id, user_id_option
        )

    return True


@v1.get(
    "/playlists/{playlist_id}",
    tags=[PLAYLISTS],
    summary="Fetches the playlist with the given ID.",
)
async def get_playlist(
    playlist_id: UUID,
    user_id_option: Optional[UUID] = Depends(optional_token_dependency),
) -> PlaylistData:
    playlist = await database.query_playlist(playlist_id)

    if playlist is None:
        raise NotFound(CAN_NOT_FIND_PLAYLIST.format(playlist_id))

    if await check_accessible(playlist, user_id_option):
        return playlist_into_data(playlist)

    raise Forbidden(INACCESSIBLE_PLAYLIST.format(playlist_id))


@v1.put(
    "/playlists/{playlist_id}",
    tags=[PLAYLISTS],
    summary="Updates the playlist with the given ID.",
)
async def update_playlist(
    playlist_id: UUID,
    user_id: UUID = Depends(token_dependency),
    name: Optional[str] = Body(default=None),
    description: Optional[str] = Body(default=None),
    privacy_type: Optional[PrivacyType] = Body(default=None),
) -> None:
    if name is None and description is None and privacy_type is None:
        return  # there is nothing to update

    playlist = await database.query_playlist(playlist_id=playlist_id)

    if playlist is None:
        raise NotFound(CAN_NOT_FIND_PLAYLIST.format(playlist_id))

    if name is None:
        name = playlist.name

    if description is None:
        description = playlist.description

    if privacy_type is None:
        privacy_type = playlist.privacy_type

    await database.update_playlist(
        playlist_id=playlist_id, name=name, description=description, privacy_type=privacy_type
    )


@v1.delete(
    "/playlists/{playlist_id}",
    tags=[PLAYLISTS],
    summary="Deletes the playlist with the given ID.",
)
async def delete_playlist(playlist_id: UUID, user_id: UUID = Depends(token_dependency)) -> None:
    if await database.check_playlist(playlist_id, user_id):
        await database.delete_playlist(playlist_id)

    else:
        raise Forbidden(INACCESSIBLE_PLAYLIST.format(playlist_id))


@v1.get(
    "/playlists/{playlist_id}/link",
    tags=[PLAYLISTS, LINKS],
    summary="Fetches the playlist link with the given ID.",
)
async def get_playlist_link(playlist_id: UUID) -> FileResponse:
    uri = URI(type=EntityType.PLAYLIST, id=playlist_id)

    path = await uri.create_link()

    return FileResponse(path)


@v1.get(
    "/playlists/{playlist_id}/image",
    tags=[PLAYLISTS, IMAGES],
    summary="Fetches the playlist image with the given ID.",
)
async def get_playlist_image(playlist_id: UUID) -> FileResponse:
    uri = URI(type=EntityType.PLAYLIST, id=playlist_id)

    path = uri.image_path_for(config.images)

    if not path.exists():
        raise NotFound(CAN_NOT_FIND_PLAYLIST_IMAGE.format(playlist_id))

    return FileResponse(path)


EXPECTED_IMAGE_TYPE = f"expected `{IMAGE_TYPE}` image type"


@v1.put(
    "/playlists/{playlist_id}/image",
    tags=[PLAYLISTS, IMAGES],
    summary="Replaces the playlist image with the given ID.",
)
async def replace_playlist_image(
    playlist_id: UUID, image: UploadFile = File(), user_id: UUID = Depends(token_dependency)
) -> None:
    if image.content_type != IMAGE_CONTENT_TYPE:
        raise ValidationError(EXPECTED_IMAGE_TYPE)

    if await database.check_playlist(playlist_id, user_id):
        uri = URI(type=EntityType.PLAYLIST, id=playlist_id)

        path = uri.image_path_for(config.images)

        file = await open_file(path, WRITE_BINARY)

        await file.write(await image.read())

    else:
        raise Forbidden(INACCESSIBLE_PLAYLIST.format(playlist_id))


@v1.get(
    "/playlists/{playlist_id}/tracks",
    tags=[PLAYLISTS, TRACKS],
    summary="Fetches playlist tracks with the given ID.",
)
async def get_playlist_tracks(
    playlist_id: UUID,
    user_id_option: Optional[UUID] = Depends(optional_token_dependency),
) -> PlaylistTracksData:
    playlist = await database.query_playlist(playlist_id)

    if playlist is None:
        raise NotFound(CAN_NOT_FIND_PLAYLIST.format(playlist_id))

    if await check_accessible(playlist, user_id_option):
        tracks = await database.query_playlist_tracks(playlist_id)

        if tracks is None:
            raise NotFound(CAN_NOT_FIND_PLAYLIST.format(playlist_id))

        return iter(tracks).map(position_track_into_data).list()

    raise Forbidden(INACCESSIBLE_PLAYLIST.format(playlist_id))
