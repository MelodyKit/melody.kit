from typing import Optional
from uuid import UUID

from fastapi import status

from melody.kit.errors.core import Error, ErrorCode
from melody.kit.errors.decorators import default_code, default_status_code

__all__ = ("AlbumError", "AlbumNotFound")


@default_code(ErrorCode.ALBUM_ERROR)
class AlbumError(Error):
    def __init__(
        self,
        album_id: UUID,
        message: str,
        code: Optional[ErrorCode] = None,
        status_code: Optional[int] = None,
    ) -> None:
        super().__init__(message, code, status_code)

        self._album_id = album_id

    @property
    def album_id(self) -> UUID:
        return self._album_id


ALBUM_NOT_FOUND = "album `{}` not found"
album_not_found = ALBUM_NOT_FOUND.format


@default_code(ErrorCode.ALBUM_NOT_FOUND)
@default_status_code(status.HTTP_404_NOT_FOUND)
class AlbumNotFound(AlbumError):
    def __init__(self, album_id: UUID) -> None:
        super().__init__(album_id, album_not_found(album_id))
