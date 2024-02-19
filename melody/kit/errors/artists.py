from typing import Optional
from uuid import UUID

from fastapi import status

from melody.kit.errors.core import Error, ErrorCode
from melody.kit.errors.decorators import default_code, default_status_code

__all__ = ("ArtistError", "ArtistNotFound")


@default_code(ErrorCode.ARTIST_ERROR)
class ArtistError(Error):
    def __init__(
        self,
        artist_id: UUID,
        message: str,
        code: Optional[ErrorCode] = None,
        status_code: Optional[int] = None,
    ) -> None:
        super().__init__(message, code, status_code)

        self._artist_id = artist_id

    @property
    def artist_id(self) -> UUID:
        return self._artist_id


ARTIST_NOT_FOUND = "artist `{}` not found"
artist_not_found = ARTIST_NOT_FOUND.format


@default_code(ErrorCode.ARTIST_NOT_FOUND)
@default_status_code(status.HTTP_404_NOT_FOUND)
class ArtistNotFound(ArtistError):
    def __init__(self, artist_id: UUID) -> None:
        super().__init__(artist_id, artist_not_found(artist_id))
