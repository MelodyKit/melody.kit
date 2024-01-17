from pathlib import Path

from colors import Color
from qrcode.image.styledpil import StyledPilImage as StyledPILImage
from qrcode.image.styles.colormasks import VerticalGradiantColorMask
from qrcode.main import QRCode

from melody.kit.core import config
from melody.kit.uri import URI
from melody.shared.asyncio import run_blocking
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
    link_config = config.link

    path = link_config.cache / image_name

    if path.exists():
        return path

    qr: QRCode[StyledPILImage] = QRCode(
        version=None,
        error_correction=link_config.error_correction.into_error_correction(),
        box_size=link_config.box_size,
        border=link_config.border,
    )

    qr.add_data(string)

    qr.make()

    image = qr.make_image(
        image_factory=StyledPILImage,  # type: ignore[type-abstract]
        color_mask=VerticalGradiantColorMask(
            back_color=TRANSPARENT,
            top_color=MELODY_PURPLE,
            bottom_color=MELODY_BLUE,
        ),
    )

    image.save(path)

    return path


def generate_code_for_uri_sync(uri: URI) -> Path:
    return generate_code_sync(str(uri), uri.image_name)


async def generate_code(string: str, image_name: str) -> Path:
    return await run_blocking(generate_code_sync, string, image_name)


async def generate_code_for_uri(uri: URI) -> Path:
    return await run_blocking(generate_code_for_uri_sync, uri)
