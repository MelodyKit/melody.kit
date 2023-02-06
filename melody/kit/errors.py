from __future__ import annotations

from enum import Enum
from typing import Any, Generic, TypeVar

from attrs import frozen
from fastapi import status
from typing_extensions import TypedDict as Data

__all__ = (
    "AnyError",
    "Error",
    "ErrorCode",
    "ErrorData",
    "AuthenticationError",
    "ValidationError",
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
    AUTHENTICATION_EXPIRED = 13603

    @classmethod
    def from_status_code(cls, status_code: int) -> ErrorCode:
        default = cls.DEFAULT

        try:
            return cls(default.value + status_code)

        except ValueError:
            return default


T = TypeVar("T")


class ErrorData(Data, Generic[T]):
    detail: T
    code: int


@frozen()
class Error(Exception, Generic[T]):
    detail: T
    code: ErrorCode = ErrorCode.DEFAULT
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def into_data(self) -> ErrorData[T]:
        return ErrorData(code=self.code.value, detail=self.detail)


AnyError = Error[Any]


@frozen()
class AuthenticationError(Error[T]):
    """Authentication has failed."""

    code: ErrorCode = ErrorCode.AUTHENTICATION_ERROR
    status_code: int = status.HTTP_401_UNAUTHORIZED


@frozen()
class ValidationError(Error[T]):
    """Validation has failed."""

    code: ErrorCode = ErrorCode.UNPROCESSABLE_ENTITY
    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY


INTERNAL_ERROR = "internal error"


@frozen()
class InternalError(Error[str]):
    """Internal error has occured."""

    detail: str = INTERNAL_ERROR
    code: ErrorCode = ErrorCode.INTERNAL_SERVER_ERROR
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
