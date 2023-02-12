from typing import Optional
from uuid import UUID

from fastapi import Depends
from fastapi.responses import FileResponse
from iters import iter

from melody.kit.core import database, v1
from melody.kit.dependencies import optional_token_dependency
from melody.kit.enums import EntityType
from melody.kit.errors import Forbidden, NotFound
from melody.kit.models.playlist import (
    Playlist,
    PlaylistData,
    PlaylistTracksData,
    playlist_into_data,
)
from melody.kit.models.track import track_into_data
from melody.kit.tags import LINKS, PLAYLISTS, TRACKS
from melody.kit.uri import URI

__all__ = ("get_playlist", "get_playlist_link", "get_playlist_tracks")

CAN_NOT_FIND_PLAYLIST = "can not find the playlist with ID `{}`"
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
        return user_id_option is not None and await database.check_friends(
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

        return iter(tracks).map(track_into_data).list()

    raise Forbidden(INACCESSIBLE_PLAYLIST.format(playlist_id))
