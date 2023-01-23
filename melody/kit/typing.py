from os import PathLike
from typing import Callable, Dict, TypeVar, Union

__all__ = (
    "Unary",
    "Predicate",
    "StringDict",
    "IntoPath",
)

T = TypeVar("T")
R = TypeVar("R")

Unary = Callable[[T], R]

Predicate = Unary[T, bool]

StringDict = Dict[str, T]

try:
    IntoPath = Union[str, PathLike[str]]  # type: ignore

except TypeError:
    IntoPath = Union[str, PathLike]  # type: ignore
