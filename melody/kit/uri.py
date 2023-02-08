from pathlib import Path
from typing import Type, TypeVar
from uuid import UUID

from async_extensions.blocking import run_blocking_in_thread
from attrs import frozen
from qrcode import QRCode  # type: ignore
from qrcode.constants import ERROR_CORRECT_H as ERROR_CORRECTION_HIGH  # type: ignore
from qrcode.image.styledpil import StyledPilImage as StyledPILImage  # type: ignore
from qrcode.image.styles.colormasks import VerticalGradiantColorMask  # type: ignore

from melody.kit.enums import URIType

__all__ = ("URI",)

# QR code constants

HOME = Path.home()

CACHE_NAME = ".cache"
MELODY = "melody"
LINK = "link"
KIT = "kit"

LINK_CACHE = HOME / CACHE_NAME / MELODY / LINK

LINK_CACHE.mkdir(parents=True, exist_ok=True)

KIT_CACHE = HOME / CACHE_NAME / MELODY / KIT

KIT_CACHE.mkdir(parents=True, exist_ok=True)

IMAGE_NAME = "{type}.{id}.png"
image_name = IMAGE_NAME.format

VERSION = None  # auto-detect version
ERROR_CORRECTION = ERROR_CORRECTION_HIGH
BOX_SIZE = 20
BORDER = 4

MELODY_PURPLE = (0xCC, 0x55, 0xFF, 0xFF)
MELODY_BLUE = (0x55, 0xCC, 0xFF, 0xFF)
TRANSPARENT = (0x00, 0x00, 0x00, 0x00)

# URI constants

HEADER = "melody.link"

URI_SEPARATOR = ":"

URI_STRING = f"{{header}}{URI_SEPARATOR}{{type}}{URI_SEPARATOR}{{id}}"
uri_string = URI_STRING.format

INVALID_HEADER = f"invalid header `{{}}`; expected `{HEADER}`"

U = TypeVar("U", bound="URI")


@frozen()
class URI:
    type: URIType
    id: UUID

    def __str__(self) -> str:
        return self.to_string()

    @classmethod
    def from_string(cls: Type[U], string: str) -> U:
        header, type_string, id_string = string.split(URI_SEPARATOR)

        if header != HEADER:
            raise ValueError(INVALID_HEADER.format(header))

        type = URIType(type_string)

        id = UUID(id_string)

        return cls(type=type, id=id)

    def to_string(self) -> str:
        return uri_string(header=HEADER, type=self.type.value, id=self.id)

    @property
    def image_name(self) -> str:
        return image_name(type=self.type.value, id=self.id)

    @property
    def link_path(self) -> Path:
        return LINK_CACHE / self.image_name

    @property
    def kit_path(self) -> Path:
        return KIT_CACHE / self.image_name

    async def create_link(self) -> Path:
        return await run_blocking_in_thread(self.create_link_sync)

    def create_link_sync(self) -> Path:
        path = self.link_path

        if path.exists():
            return path

        qr = QRCode(
            version=VERSION, error_correction=ERROR_CORRECTION, box_size=BOX_SIZE, border=BORDER
        )

        qr.add_data(self.to_string())

        qr.make()

        image = qr.make_image(
            image_factory=StyledPILImage,
            color_mask=VerticalGradiantColorMask(
                back_color=TRANSPARENT,
                top_color=MELODY_PURPLE,
                bottom_color=MELODY_BLUE,
            ),
        )

        image.save(path)

        return path
