from os import PathLike
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union

__all__ = (
    "Unary",
    "Predicate",
    "StringDict",
    "Primitive",
    "Parameters",
    "Headers",
    "Payload",
    "IntoPath",
)

T = TypeVar("T")
R = TypeVar("R")

Unary = Callable[[T], R]

Predicate = Unary[T, bool]

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
