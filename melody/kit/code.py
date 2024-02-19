from pathlib import Path

from async_extensions import run_blocking_in_thread
from colors import Color
from qrcode.image.svg import SvgPathFillImage as SVGPathFillImage
from qrcode.main import QRCode

from melody.kit.core import config
from melody.kit.uri import URI
from melody.shared.constants import MELODY_BLUE, MELODY_PURPLE, ZERO

__all__ = (
    "generate_code",
    "generate_code_sync",
    "generate_code_for_uri",
    "generate_code_for_uri_sync",
)

# color constants

TOP_COLOR = MELODY_PURPLE.to_rgba()
BOTTOM_COLOR = MELODY_BLUE.to_rgba()

TRANSPARENT = Color.black().to_rgba(ZERO)


def generate_code_sync(string: str, image_name: str) -> Path:
    code_config = config.code

    path = code_config.cache / image_name

    if path.exists():
        return path

    qr: QRCode[SVGPathFillImage] = QRCode(
        version=None,
        error_correction=code_config.error_correction.into_error_correction(),
        box_size=code_config.box_size,
        border=code_config.border,
        image_factory=SVGPathFillImage,
    )

    qr.add_data(string)

    qr.make()

    qr.make_image().save(path)

    return path


def generate_code_for_uri_sync(uri: URI) -> Path:
    return generate_code_sync(str(uri), uri.image_name)


async def generate_code(string: str, image_name: str) -> Path:
    return await run_blocking_in_thread(generate_code_sync, string, image_name)


async def generate_code_for_uri(uri: URI) -> Path:
    return await run_blocking_in_thread(generate_code_for_uri_sync, uri)
