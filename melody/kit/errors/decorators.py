from typing import TypeVar, final

from attrs import frozen

from melody.kit.errors.core import ErrorCode, ErrorType

__all__ = ("default_code", "default_status_code")

ET = TypeVar("ET", bound=ErrorType)


@final
@frozen()
class DefaultCode:
    code: ErrorCode

    def __call__(self, error_type: ET) -> ET:
        error_type.DEFAULT_CODE = self.code

        return error_type


def default_code(code: ErrorCode) -> DefaultCode:
    return DefaultCode(code)


@final
@frozen()
class DefaultStatusCode:
    status_code: int

    def __call__(self, error_type: ET) -> ET:
        error_type.DEFAULT_STATUS_CODE = self.status_code

        return error_type


def default_status_code(status_code: int) -> DefaultStatusCode:
    return DefaultStatusCode(status_code)
