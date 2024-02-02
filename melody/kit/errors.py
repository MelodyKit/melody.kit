from __future__ import annotations

from enum import Enum
from typing import ClassVar

from fastapi import status
from typing_aliases import NormalError

from melody.shared.typing import Data

__all__ = (
    "Error",
    "ErrorCode",
    "ErrorData",
    "AuthError",
    "AuthExpected",
    "AuthInvalid",
    "ValidationError",
    "BadRequest",
    "Unauthorized",
    "Forbidden",
    "NotFound",
    "MethodNotAllowed",
    "Conflict",
    "Gone",
    "PayloadTooLarge",
    "RateLimited",
    "InternalError",
)


class ErrorCode(Enum):
    DEFAULT = 13000

    BAD_REQUEST = 13400
    UNAUTHORIZED = 13401
    FORBIDDEN = 13403
    NOT_FOUND = 13404
    METHOD_NOT_ALLOWED = 13405
    CONFLICT = 13409
    GONE = 13410
    PAYLOAD_TOO_LARGE = 13413
    UNPROCESSABLE_ENTITY = 13422
    TOO_MANY_REQUESTS = 13429

    INTERNAL_SERVER_ERROR = 13500

    AUTH_ERROR = 13600
    AUTH_EXPECTED = 13601
    AUTH_INVALID = 13602

    @classmethod
    def from_status_code(cls, status_code: int) -> ErrorCode:
        default = cls.DEFAULT

        try:
            return cls(default.value + status_code)

        except ValueError:
            return default


class ErrorData(Data):
    code: int
    message: str


class Error(NormalError):
    CODE: ClassVar[ErrorCode] = ErrorCode.DEFAULT
    STATUS_CODE: ClassVar[int] = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message: str) -> None:
        super().__init__(message)

        self._message = message

    @property
    def message(self) -> str:
        return self._message

    def into_data(self) -> ErrorData:
        return ErrorData(code=self.CODE.value, message=self.message)


class AuthError(Error):
    """Authentication has failed."""

    CODE: ClassVar[ErrorCode] = ErrorCode.AUTH_ERROR
    STATUS_CODE: ClassVar[int] = status.HTTP_401_UNAUTHORIZED


class AuthExpected(AuthError):
    """Authentication was expected."""

    CODE: ClassVar[ErrorCode] = ErrorCode.AUTH_EXPECTED


class AuthInvalid(AuthError):
    """Authentication is invalid."""

    CODE: ClassVar[ErrorCode] = ErrorCode.AUTH_INVALID


class ValidationError(Error):
    """Validation has failed."""

    CODE: ClassVar[ErrorCode] = ErrorCode.UNPROCESSABLE_ENTITY
    STATUS_CODE: ClassVar[int] = status.HTTP_422_UNPROCESSABLE_ENTITY


class BadRequest(Error):
    """Bad request."""

    CODE: ClassVar[ErrorCode] = ErrorCode.BAD_REQUEST
    STATUS_CODE: ClassVar[int] = status.HTTP_400_BAD_REQUEST


class Unauthorized(Error):
    """User is unauthorized."""

    CODE: ClassVar[ErrorCode] = ErrorCode.UNAUTHORIZED
    STATUS_CODE: ClassVar[int] = status.HTTP_401_UNAUTHORIZED


class Forbidden(Error):
    """Access is forbidden."""

    CODE: ClassVar[ErrorCode] = ErrorCode.FORBIDDEN
    STATUS_CODE: ClassVar[int] = status.HTTP_403_FORBIDDEN


class NotFound(Error):
    """Item was not found."""

    CODE: ClassVar[ErrorCode] = ErrorCode.NOT_FOUND
    STATUS_CODE: ClassVar[int] = status.HTTP_404_NOT_FOUND


class MethodNotAllowed(Error):
    """Method is not allowed."""

    CODE: ClassVar[ErrorCode] = ErrorCode.METHOD_NOT_ALLOWED
    STATUS_CODE: ClassVar[int] = status.HTTP_405_METHOD_NOT_ALLOWED


class Conflict(Error):
    """Conflict has occured."""

    CODE: ClassVar[ErrorCode] = ErrorCode.CONFLICT
    STATUS_CODE: ClassVar[int] = status.HTTP_409_CONFLICT


class Gone(Error):
    """Item is gone."""

    CODE: ClassVar[ErrorCode] = ErrorCode.GONE
    STATUS_CODE: ClassVar[int] = status.HTTP_410_GONE


class PayloadTooLarge(Error):
    """Payload is too large."""

    CODE: ClassVar[ErrorCode] = ErrorCode.PAYLOAD_TOO_LARGE
    STATUS_CODE: ClassVar[int] = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE


class RateLimited(Error):
    """Rate limit has occured."""

    CODE: ClassVar[ErrorCode] = ErrorCode.TOO_MANY_REQUESTS
    STATUS_CODE: ClassVar[int] = status.HTTP_429_TOO_MANY_REQUESTS


UNHANDLED_ERROR = "unhandled error"


class InternalError(Error):
    """Internal error has occured."""

    CODE: ClassVar[ErrorCode] = ErrorCode.INTERNAL_SERVER_ERROR
    STATUS_CODE: ClassVar[int] = status.HTTP_500_INTERNAL_SERVER_ERROR
