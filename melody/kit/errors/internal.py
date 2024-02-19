from fastapi import status

from melody.kit.errors.core import Error, ErrorCode
from melody.kit.errors.decorators import default_code, default_status_code

__all__ = ("InternalError",)

INTERNAL_ERROR = "internal error"


@default_code(ErrorCode.INTERNAL_SERVER_ERROR)
@default_status_code(status.HTTP_500_INTERNAL_SERVER_ERROR)
class InternalError(Error):
    def __init__(self) -> None:
        super().__init__(INTERNAL_ERROR)
