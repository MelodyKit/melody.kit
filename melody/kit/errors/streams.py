from typing import Optional
from uuid import UUID

from fastapi import status

from melody.kit.errors.core import Error, ErrorCode
from melody.kit.errors.decorators import default_code, default_status_code

__all__ = ("StreamError", "StreamNotFound", "StreamInaccessible")


@default_code(ErrorCode.STREAM_ERROR)
class StreamError(Error):
    def __init__(
        self,
        stream_id: UUID,
        message: str,
        code: Optional[ErrorCode] = None,
        status_code: Optional[int] = None,
    ) -> None:
        super().__init__(message, code, status_code)

        self._stream_id = stream_id

    @property
    def stream_id(self) -> UUID:
        return self._stream_id


STREAM_NOT_FOUND = "stream `{}` not found"
stream_not_found = STREAM_NOT_FOUND.format


@default_code(ErrorCode.STREAM_NOT_FOUND)
@default_status_code(status.HTTP_404_NOT_FOUND)
class StreamNotFound(StreamError):
    def __init__(self, stream_id: UUID) -> None:
        super().__init__(stream_id, stream_not_found(stream_id))


STREAM_INACCESSIBLE = "stream `{}` is inaccessible"
stream_inaccessible = STREAM_INACCESSIBLE.format


@default_code(ErrorCode.STREAM_INACCESSIBLE)
@default_status_code(status.HTTP_403_FORBIDDEN)
class StreamInaccessible(StreamError):
    def __init__(self, stream_id: UUID) -> None:
        super().__init__(stream_id, stream_inaccessible(stream_id))
