from typing import Union

from typing_extensions import TypedDict as Data
from yarl import URL

__all__ = (
    "Data",
    "URLString",
    "AnyString",
)

URLString = Union[URL, str]
AnyString = Union[str, bytes]
