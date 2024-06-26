from typing import Union

from typing_extensions import TypedDict as Data
from yarl import URL

__all__ = ("Data", "URLString", "IntString")

URLString = Union[URL, str]
IntString = Union[int, str]
