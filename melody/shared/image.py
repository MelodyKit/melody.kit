from io import BytesIO
from pathlib import Path

from async_extensions.file import open_file
from fastapi import UploadFile
from PIL.Image import open as open_image

from melody.shared.constants import IMAGE_CONTENT_TYPE, WRITE_BINARY

__all__ = ("check_image_type", "validate_and_save_image")


def check_image_type(upload_file: UploadFile) -> bool:
    return upload_file.content_type == IMAGE_CONTENT_TYPE


async def validate_and_save_image(upload_file: UploadFile, path: Path) -> bool:
    data = await upload_file.read()

    buffer = BytesIO(data)

    image = open_image(buffer)

    check = image.width == image.height

    if check:
        file = await open_file(path, WRITE_BINARY)

        await file.write(data)

    return check