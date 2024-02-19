from typing import Optional
from uuid import UUID

from fastapi import status

from melody.kit.errors.core import Error, ErrorCode
from melody.kit.errors.decorators import default_code, default_status_code

__all__ = ("ClientError", "ClientNotFound", "ClientInaccessible")


@default_code(ErrorCode.CLIENT_ERROR)
class ClientError(Error):
    def __init__(
        self,
        client_id: UUID,
        message: str,
        code: Optional[ErrorCode] = None,
        status_code: Optional[int] = None,
    ) -> None:
        super().__init__(message, code, status_code)

        self._client_id = client_id

    @property
    def client_id(self) -> UUID:
        return self._client_id


CLIENT_NOT_FOUND = "client `{}` not found"
client_not_found = CLIENT_NOT_FOUND.format


@default_code(ErrorCode.CLIENT_NOT_FOUND)
@default_status_code(status.HTTP_404_NOT_FOUND)
class ClientNotFound(ClientError):
    def __init__(self, client_id: UUID) -> None:
        super().__init__(client_id, client_not_found(client_id))


CLIENT_INACCESSIBLE = "client `{}` is inaccessible"
client_inaccessible = CLIENT_INACCESSIBLE.format


@default_code(ErrorCode.CLIENT_INACCESSIBLE)
@default_status_code(status.HTTP_403_FORBIDDEN)
class ClientInaccessible(ClientError):
    def __init__(self, client_id: UUID) -> None:
        super().__init__(client_id, client_inaccessible(client_id))
