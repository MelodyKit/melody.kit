from typing import Optional
from uuid import UUID

from fastapi import status

from melody.kit.errors.core import Error, ErrorCode
from melody.kit.errors.decorators import default_code, default_status_code

__all__ = ("TrackError", "TrackNotFound")


@default_code(ErrorCode.TRACK_ERROR)
class TrackError(Error):
    def __init__(
        self,
        track_id: UUID,
        message: str,
        code: Optional[ErrorCode] = None,
        status_code: Optional[int] = None,
    ) -> None:
        super().__init__(message, code, status_code)

        self._track_id = track_id

    @property
    def track_id(self) -> UUID:
        return self._track_id


TRACK_NOT_FOUND = "track `{}` not found"
track_not_found = TRACK_NOT_FOUND.format


@default_code(ErrorCode.TRACK_NOT_FOUND)
@default_status_code(status.HTTP_404_NOT_FOUND)
class TrackNotFound(TrackError):
    def __init__(self, track_id: UUID) -> None:
        super().__init__(track_id, track_not_found(track_id))
