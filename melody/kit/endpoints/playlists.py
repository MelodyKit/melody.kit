from typing import Optional
from uuid import UUID

from fastapi import Depends, status
from fastapi.responses import FileResponse
from iters import iter

from melody.kit.core import database, v1
from melody.kit.dependencies import optional_token_dependency
from melody.kit.enums import URIType
from melody.kit.errors import Error, ErrorCode
from melody.kit.models import Playlist, PlaylistData, PlaylistTracksData, track_into_data
from melody.kit.uri import URI

__all__ = ("get_playlist", "get_playlist_link", "get_playlist_tracks")

CAN_NOT_FIND_PLAYLIST = "can not find the playlist with id `{}`"
INACCESSIBLE_PLAYLIST = "the playlist with id `{}` is inaccessible"


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


@v1.get("/playlists/{playlist_id}")
async def get_playlist(
    playlist_id: UUID,
    user_id_option: Optional[UUID] = Depends(optional_token_dependency),
) -> PlaylistData:
    playlist = await database.query_playlist(playlist_id)

    if playlist is None:
        raise Error(
            CAN_NOT_FIND_PLAYLIST.format(playlist_id),
            ErrorCode.NOT_FOUND,
            status.HTTP_404_NOT_FOUND,
        )

    if await check_accessible(playlist, user_id_option):
        return playlist.into_data()

    raise Error(
        INACCESSIBLE_PLAYLIST.format(playlist_id),
        ErrorCode.FORBIDDEN,
        status.HTTP_403_FORBIDDEN,
    )


@v1.get("/playlists/{playlist_id}/link")
async def get_playlist_link(playlist_id: UUID) -> FileResponse:
    uri = URI(type=URIType.PLAYLIST, id=playlist_id)

    path = await uri.create_link()

    return FileResponse(path)


@v1.get("/playlists/{playlist_id}/tracks")
async def get_playlist_tracks(
    playlist_id: UUID,
    user_id_option: Optional[UUID] = Depends(optional_token_dependency),
) -> PlaylistTracksData:
    playlist = await database.query_playlist(playlist_id)

    if playlist is None:
        raise Error(
            CAN_NOT_FIND_PLAYLIST.format(playlist_id),
            ErrorCode.NOT_FOUND,
            status.HTTP_404_NOT_FOUND,
        )

    if await check_accessible(playlist, user_id_option):
        tracks = await database.query_playlist_tracks(playlist_id)

        if tracks is None:
            raise Error(
                CAN_NOT_FIND_PLAYLIST.format(playlist_id),
                ErrorCode.NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            )

        return iter(tracks).map(track_into_data).list()

    raise Error(
        INACCESSIBLE_PLAYLIST.format(playlist_id),
        ErrorCode.FORBIDDEN,
        status.HTTP_403_FORBIDDEN,
    )
