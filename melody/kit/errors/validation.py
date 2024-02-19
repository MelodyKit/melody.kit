from fastapi import status
from fastapi.exceptions import RequestValidationError
from typing_extensions import Self

from melody.kit.errors.core import Error, ErrorCode
from melody.kit.errors.decorators import default_code, default_status_code

__all__ = ("ValidationError",)


@default_code(ErrorCode.VALIDATION_ERROR)
@default_status_code(status.HTTP_422_UNPROCESSABLE_ENTITY)
class ValidationError(Error):
    @classmethod
    def from_error(cls, error: RequestValidationError) -> Self:
        return cls(str(error))
