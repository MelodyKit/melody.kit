from typing import Type, TypeVar
from uuid import UUID

from cattrs import Converter
from yarl import URL

__all__ = ("CONVERTER",)

CONVERTER = Converter()

U = TypeVar("U", bound=UUID)


def structure_uuid(string: str, cls: Type[U]) -> U:
    return cls(string)


def unstructure_uuid(uuid: UUID) -> str:
    return str(uuid)


CONVERTER.register_structure_hook(UUID, structure_uuid)
CONVERTER.register_unstructure_hook(UUID, unstructure_uuid)


V = TypeVar("V", bound="URL")


def structure_url(string: str, cls: Type[V]) -> V:
    return cls(string)


def unstructure_url(url: URL) -> str:
    return str(url)


CONVERTER.register_structure_hook(URL, structure_url)
CONVERTER.register_unstructure_hook(URL, unstructure_url)
