from typing import ClassVar, Protocol, Type, TypeVar
from uuid import UUID

from attrs import frozen
from typing_extensions import Self

from melody.kit.enums import EntityType
from melody.shared.constants import CODE_TYPE
from melody.shared.converter import CONVERTER

__all__ = ("URI", "URI_HEADER", "URI_SEPARATOR", "Locatable")

# image constants

IMAGE_NAME = f"{{type}}.{{id}}.{CODE_TYPE}"
image_name = IMAGE_NAME.format

# URI constants

URI_HEADER = "melody.kit"

URI_SEPARATOR = ":"

URI_STRING = f"{{header}}{URI_SEPARATOR}{{type}}{URI_SEPARATOR}{{id}}"
uri_string = URI_STRING.format

INVALID_URI_HEADER = f"invalid header `{{}}`; expected `{URI_HEADER}`"
invalid_uri_header = INVALID_URI_HEADER.format

U = TypeVar("U", bound="URI")


@frozen()
class URI:
    type: EntityType
    id: UUID

    def __str__(self) -> str:
        return self.to_string()

    @classmethod
    def from_string(cls, string: str) -> Self:
        header, type_string, id_string = string.split(URI_SEPARATOR)

        if header != URI_HEADER:
            raise ValueError(invalid_uri_header(header))

        type = EntityType(type_string)

        id = UUID(id_string)

        return cls(type=type, id=id)

    def to_string(self) -> str:
        return uri_string(header=URI_HEADER, type=self.type.value, id=self.id)

    @property
    def image_name(self) -> str:
        return image_name(type=self.type.value, id=self.id)


def structure_uri(string: str, uri_type: Type[U]) -> U:
    return uri_type.from_string(string)


def unstructure_uri(uri: URI) -> str:
    return uri.to_string()


CONVERTER.register_structure_hook(URI, structure_uri)
CONVERTER.register_unstructure_hook(URI, unstructure_uri)


class Locatable(Protocol):
    TYPE: ClassVar[EntityType]

    id: UUID

    @property
    def uri(self) -> URI:
        return URI(type=self.TYPE, id=self.id)
