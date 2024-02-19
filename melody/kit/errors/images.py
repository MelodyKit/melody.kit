from fastapi import status

from melody.kit.errors.core import Error, ErrorCode
from melody.kit.errors.decorators import default_code, default_status_code

__all__ = ("ImageError", "ImageUnexpectedType", "ImageExpectedSquare", "ImageTooLarge")


@default_code(ErrorCode.IMAGE_ERROR)
class ImageError(Error):
    pass


UNEXPECTED_IMAGE_TYPE = "unexpected image type"


@default_code(ErrorCode.IMAGE_UNEXPECTED_TYPE)
@default_status_code(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
class ImageUnexpectedType(Error):
    def __init__(self) -> None:
        super().__init__(UNEXPECTED_IMAGE_TYPE)


EXPECTED_SQUARE_IMAGE = "expected square image"


@default_code(ErrorCode.IMAGE_EXPECTED_SQUARE)
@default_status_code(status.HTTP_422_UNPROCESSABLE_ENTITY)
class ImageExpectedSquare(Error):
    def __init__(self) -> None:
        super().__init__(EXPECTED_SQUARE_IMAGE)


IMAGE_TOO_LARGE = "the image is too large"


@default_code(ErrorCode.IMAGE_TOO_LARGE)
@default_status_code(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
class ImageTooLarge(Error):
    def __init__(self) -> None:
        super().__init__(IMAGE_TOO_LARGE)
