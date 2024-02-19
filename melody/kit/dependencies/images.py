from fastapi import Depends
from PIL.Image import open as open_image
from typing_extensions import Annotated

from melody.kit.core import config
from melody.kit.dependencies.common import FileDependency
from melody.kit.errors.images import ImageExpectedSquare, ImageTooLarge, ImageUnexpectedType
from melody.shared.constants import CHUNK_SIZE, IMAGE_CONTENT_TYPE

__all__ = (
    # dependencies
    "ImageDependency",
    # dependables
    "image_dependency",
)


async def image_dependency(file: FileDependency) -> bytes:
    if file.content_type != IMAGE_CONTENT_TYPE:
        raise ImageUnexpectedType()

    image_config = config.image

    data_size_limit = image_config.data_size_limit
    size_limit = image_config.size_limit

    chunk_size = CHUNK_SIZE

    data = bytes()
    size = 0

    while True:
        chunk = await file.read(chunk_size)

        if not chunk:
            break

        data += chunk

        size += len(chunk)

        if size > data_size_limit:
            raise ImageTooLarge()

    image = open_image(data)

    width = image.width
    height = image.height

    if width > size_limit or height > size_limit:
        raise ImageTooLarge()

    if width != height:
        raise ImageExpectedSquare()

    return data


ImageDependency = Annotated[bytes, Depends(image_dependency)]
