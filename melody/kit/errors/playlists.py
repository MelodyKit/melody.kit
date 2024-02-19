from typing import Optional
from uuid import UUID

from fastapi import status

from melody.kit.errors.core import Error, ErrorCode
from melody.kit.errors.decorators import default_code, default_status_code

__all__ = (
    "PlaylistError",
    "PlaylistNotFound",
    "PlaylistInaccessible",
    "PlaylistImageNotFound",
)


@default_code(ErrorCode.PLAYLIST_ERROR)
class PlaylistError(Error):
    def __init__(
        self,
        playlist_id: UUID,
        message: str,
        code: Optional[ErrorCode] = None,
        status_code: Optional[int] = None,
    ) -> None:
        super().__init__(message, code, status_code)

        self._playlist_id = playlist_id

    @property
    def playlist_id(self) -> UUID:
        return self._playlist_id


PLAYLIST_NOT_FOUND = "playlist `{}` not found"
playlist_not_found = PLAYLIST_NOT_FOUND.format


@default_code(ErrorCode.PLAYLIST_NOT_FOUND)
@default_status_code(status.HTTP_404_NOT_FOUND)
class PlaylistNotFound(PlaylistError):
    def __init__(self, playlist_id: UUID) -> None:
        super().__init__(playlist_id, playlist_not_found(playlist_id))


PLAYLIST_INACCESSIBLE = "playlist `{}` is inaccessible"
playlist_inaccessible = PLAYLIST_INACCESSIBLE.format


@default_code(ErrorCode.PLAYLIST_INACCESSIBLE)
@default_status_code(status.HTTP_403_FORBIDDEN)
class PlaylistInaccessible(PlaylistError):
    def __init__(self, playlist_id: UUID) -> None:
        super().__init__(playlist_id, playlist_inaccessible(playlist_id))


PLAYLIST_IMAGE_NOT_FOUND = "playlist `{}` image not found"
playlist_image_not_found = PLAYLIST_IMAGE_NOT_FOUND.format


@default_code(ErrorCode.PLAYLIST_IMAGE_NOT_FOUND)
@default_status_code(status.HTTP_404_NOT_FOUND)
class PlaylistImageNotFound(PlaylistError):
    def __init__(self, playlist_id: UUID) -> None:
        super().__init__(playlist_id, playlist_image_not_found(playlist_id))
