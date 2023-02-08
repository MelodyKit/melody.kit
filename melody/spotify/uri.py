from typing import Type, TypeVar

from attrs import frozen

from melody.spotify.enums import URIType

__all__ = ("URI",)

HEADER = "spotify"

URI_SEPARATOR = ":"

URI_STRING = f"{{header}}{URI_SEPARATOR}{{type}}{URI_SEPARATOR}{{id}}"
uri_string = URI_STRING.format

INVALID_HEADER = f"invalid header `{{}}`; expected `{HEADER}`"

U = TypeVar("U", bound="URI")


@frozen()
class URI:
    type: URIType
    id: str

    def __str__(self) -> str:
        return self.to_string()

    @classmethod
    def from_string(cls: Type[U], string: str) -> U:
        header, type_string, id = string.split(URI_SEPARATOR)

        if header != HEADER:
            raise ValueError(INVALID_HEADER.format(header))

        type = URIType(type_string)

        return cls(type=type, id=id)

    def to_string(self) -> str:
        return uri_string(header=HEADER, type=self.type.value, id=self.id)
