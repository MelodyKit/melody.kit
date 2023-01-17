from __future__ import annotations

from enum import Enum
from typing import Generic, TypeVar

from attrs import frozen
from typing_extensions import TypedDict

__all__ = ("Error", "ErrorCode", "ErrorData")


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

    @classmethod
    def from_status_code(cls, status_code: int) -> ErrorCode:
        default = cls.DEFAULT

        try:
            return cls(default.value + status_code)

        except ValueError:
            return default


T = TypeVar("T")


class ErrorData(TypedDict, Generic[T]):
    code: int
    detail: T


@frozen()
class Error(Exception, Generic[T]):
    code: ErrorCode
    detail: T

    def into_data(self) -> ErrorData[T]:
        return ErrorData(code=self.code.value, detail=self.detail)
