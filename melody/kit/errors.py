from __future__ import annotations

from enum import Enum

from attrs import frozen
from fastapi import status
from typing_aliases import NormalError, Payload

from melody.shared.typing import Data

__all__ = (
    "Error",
    "ErrorCode",
    "ErrorData",
    "AuthenticationError",
    "AuthenticationInvalid",
    "AuthenticationMissing",
    "AuthenticationNotFound",
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

    AUTHENTICATION_ERROR = 13600
    AUTHENTICATION_INVALID = 13601
    AUTHENTICATION_MISSING = 13602
    AUTHENTICATION_NOT_FOUND = 13603

    @classmethod
    def from_status_code(cls, status_code: int) -> ErrorCode:
        default = cls.DEFAULT

        try:
            return cls(default.value + status_code)

        except ValueError:
            return default


class ErrorData(Data):
    detail: Payload
    code: int


@frozen()
class Error(NormalError):
    detail: Payload
    code: ErrorCode = ErrorCode.DEFAULT
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def into_data(self) -> ErrorData:
        return ErrorData(code=self.code.value, detail=self.detail)


@frozen()
class AuthenticationError(Error):
    """Authentication has failed."""

    code: ErrorCode = ErrorCode.AUTHENTICATION_ERROR
    status_code: int = status.HTTP_401_UNAUTHORIZED


@frozen()
class AuthenticationInvalid(AuthenticationError):
    """Authentication is invalid."""

    code: ErrorCode = ErrorCode.AUTHENTICATION_INVALID


@frozen()
class AuthenticationMissing(AuthenticationError):
    """Authentication is missing."""

    code: ErrorCode = ErrorCode.AUTHENTICATION_MISSING


@frozen()
class AuthenticationNotFound(AuthenticationError):
    """Authentication was not found."""

    code: ErrorCode = ErrorCode.AUTHENTICATION_NOT_FOUND


@frozen()
class ValidationError(Error):
    """Validation has failed."""

    code: ErrorCode = ErrorCode.UNPROCESSABLE_ENTITY
    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY


@frozen()
class BadRequest(Error):
    """Bad request."""

    code: ErrorCode = ErrorCode.BAD_REQUEST
    status_code: int = status.HTTP_400_BAD_REQUEST


@frozen()
class Unauthorized(Error):
    """User is unauthorized."""

    code: ErrorCode = ErrorCode.UNAUTHORIZED
    status_code: int = status.HTTP_401_UNAUTHORIZED


@frozen()
class Forbidden(Error):
    """Access is forbidden."""

    code: ErrorCode = ErrorCode.FORBIDDEN
    status_code: int = status.HTTP_403_FORBIDDEN


@frozen()
class NotFound(Error):
    """Item was not found."""

    code: ErrorCode = ErrorCode.NOT_FOUND
    status_code: int = status.HTTP_404_NOT_FOUND


@frozen()
class MethodNotAllowed(Error):
    """Method is not allowed."""

    code: ErrorCode = ErrorCode.METHOD_NOT_ALLOWED
    status_code: int = status.HTTP_405_METHOD_NOT_ALLOWED


@frozen()
class Conflict(Error):
    """Conflict has occured."""

    code: ErrorCode = ErrorCode.CONFLICT
    status_code: int = status.HTTP_409_CONFLICT


@frozen()
class Gone(Error):
    """Item is gone."""

    code: ErrorCode = ErrorCode.GONE
    status_code: int = status.HTTP_410_GONE


@frozen()
class PayloadTooLarge(Error):
    """Payload is too large."""

    code: ErrorCode = ErrorCode.PAYLOAD_TOO_LARGE
    status_code: int = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE


@frozen()
class RateLimited(Error):
    """Rate limit has occured."""

    code: ErrorCode = ErrorCode.TOO_MANY_REQUESTS
    status_code: int = status.HTTP_429_TOO_MANY_REQUESTS


INTERNAL_ERROR = "internal error"


@frozen()
class InternalError(Error):
    """Internal error has occured."""

    detail: str = INTERNAL_ERROR
    code: ErrorCode = ErrorCode.INTERNAL_SERVER_ERROR
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
