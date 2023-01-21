from typing import Optional
from uuid import UUID

from fastapi import Depends, status

from melody.kit.core import database, v1
from melody.kit.dependencies import optional_token_dependency
from melody.kit.errors import Error, ErrorCode
from melody.kit.models import PlaylistData

__all__ = ("get_playlist",)

CAN_NOT_FIND_PLAYLIST = "can not find the playlist with id `{}`"
INACCESSIBLE_PLAYLIST = "the playlist with id `{}` is inaccessible"


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

    playlist_user = playlist.user
    playlist_user_id = playlist_user.id

    if user_id_option is not None:
        if user_id_option == playlist_user_id:
            return playlist.into_data()

    playlist_privacy_type = playlist.privacy_type
    playlist_user_privacy_type = playlist_user.privacy_type

    private = playlist_privacy_type.is_private() or playlist_user_privacy_type.is_private()
    friends = playlist_privacy_type.is_friends() or playlist_user_privacy_type.is_friends()

    if private:
        raise Error(
            INACCESSIBLE_PLAYLIST.format(playlist_id),
            ErrorCode.FORBIDDEN,
            status.HTTP_403_FORBIDDEN,
        )

    if friends:
        if user_id_option is None or not await database.check_friends(
            playlist_user_id, user_id_option
        ):
            raise Error(
                INACCESSIBLE_PLAYLIST.format(playlist_id),
                ErrorCode.FORBIDDEN,
                status.HTTP_403_FORBIDDEN,
            )

    return playlist.into_data()
