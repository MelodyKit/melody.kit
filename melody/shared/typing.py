from builtins import isinstance as is_instance
from os import PathLike
from typing import Any, Callable, Dict, Iterable, List, Optional, TypeVar, Union

from typing_extensions import TypeGuard

__all__ = (
    "Unary",
    "Predicate",
    "MaybeIterable",
    "StringDict",
    "Primitive",
    "Parameters",
    "Headers",
    "Payload",
    "IntoPath",
    "is_instance",
    "is_string",
)

T = TypeVar("T")
R = TypeVar("R")

Unary = Callable[[T], R]

Predicate = Unary[T, bool]

MaybeIterable = Union[T, Iterable[T]]

StringDict = Dict[str, T]

Primitive = Optional[Union[bool, int, float, str]]

Parameters = StringDict[Any]
Headers = StringDict[Any]
Payload = Union[Primitive, List[Any], StringDict[Any]]

Response = Union[Payload, str, bytes]

try:
    IntoPath = Union[str, PathLike[str]]  # type: ignore

except TypeError:
    IntoPath = Union[str, PathLike]  # type: ignore


def is_string(item: Any) -> TypeGuard[str]:
    return is_instance(item, str)
