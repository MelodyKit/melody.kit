from typing import Type, TypeVar
from uuid import UUID

from attrs import field, frozen
from cattrs import Converter
from cattrs.gen import AttributeOverride, make_dict_structure_fn, make_dict_unstructure_fn, override
from typing_aliases import AnyType, StringDict
from yarl import URL

__all__ = (
    "CONVERTER",
    "register_structure_hook",
    "register_unstructure_hook",
    "register_unstructure_hook_omit_client",  # since clients should be omitted from the output
)

CONVERTER = Converter()


U = TypeVar("U", bound=UUID)


def structure_uuid(string: str, uuid_type: Type[U]) -> U:
    return uuid_type(string)


def unstructure_uuid(uuid: UUID) -> str:
    return str(uuid)


CONVERTER.register_structure_hook(UUID, structure_uuid)
CONVERTER.register_unstructure_hook(UUID, unstructure_uuid)


def structure_url_ignore_type(string: str, url_type: Type[URL]) -> URL:
    return URL(string)


def unstructure_url(url: URL) -> str:
    return url.human_repr()


CONVERTER.register_structure_hook(URL, structure_url_ignore_type)
CONVERTER.register_unstructure_hook(URL, unstructure_url)


AttributeOverrides = StringDict[AttributeOverride]

T = TypeVar("T", bound=AnyType)


@frozen()
class RegisterStructureHook:
    overrides: AttributeOverrides = field(factory=dict, repr=False)

    def __call__(self, type: T) -> T:
        CONVERTER.register_structure_hook(
            type, make_dict_structure_fn(type, CONVERTER, **self.overrides)  # type: ignore
        )

        return type


def register_structure_hook(**overrides: AttributeOverride) -> RegisterStructureHook:
    return RegisterStructureHook(overrides)


@frozen()
class RegisterUnstructureHook:
    overrides: AttributeOverrides = field(factory=dict, repr=False)

    def __call__(self, type: T) -> T:
        CONVERTER.register_unstructure_hook(
            type, make_dict_unstructure_fn(type, CONVERTER, **self.overrides)  # type: ignore
        )

        return type


def register_unstructure_hook(**overrides: AttributeOverride) -> RegisterUnstructureHook:
    return RegisterUnstructureHook(overrides)


register_unstructure_hook_omit_client = register_unstructure_hook(
    client_unchecked=override(omit=True)
)
