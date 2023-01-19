from os import PathLike
from typing import Dict, TypeVar, Union

__all__ = ("IntoPath", "StringDict")

T = TypeVar("T")

StringDict = Dict[str, T]

try:
    IntoPath = Union[str, PathLike[str]]  # type: ignore

except TypeError:
    IntoPath = Union[str, PathLike]  # type: ignore
