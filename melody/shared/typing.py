from typing import Literal, Union

from typing_aliases import Binary, IntoPath
from typing_extensions import TypedDict as Data
from yarl import URL

__all__ = (
    "Data",
    "URLString",
    "AnyString",
    "FileDescriptorOrIntoPath",
    "FileOpener",
    "OpenTextModeUpdating",
    "OpenTextModeWriting",
    "OpenTextModeReading",
    "OpenTextMode",
    "OpenBinaryModeUpdating",
    "OpenBinaryModeWriting",
    "OpenBinaryModeReading",
    "OpenBinaryMode",
    "OpenMode",
)

URLString = Union[URL, str]
AnyString = Union[str, bytes]

FileDescriptor = int
FileFlags = int
FilePath = str

FileDescriptorOrIntoPath = Union[FileDescriptor, IntoPath]

FileOpener = Binary[FilePath, FileFlags, FileDescriptor]

OpenTextModeUpdating = Literal[
    "r+",
    "+r",
    "rt+",
    "r+t",
    "+rt",
    "tr+",
    "t+r",
    "+tr",
    "w+",
    "+w",
    "wt+",
    "w+t",
    "+wt",
    "tw+",
    "t+w",
    "+tw",
    "a+",
    "+a",
    "at+",
    "a+t",
    "+at",
    "ta+",
    "t+a",
    "+ta",
    "x+",
    "+x",
    "xt+",
    "x+t",
    "+xt",
    "tx+",
    "t+x",
    "+tx",
]
OpenTextModeWriting = Literal["w", "wt", "tw", "a", "at", "ta", "x", "xt", "tx"]
OpenTextModeReading = Literal["r", "rt", "tr"]
OpenTextMode = Union[OpenTextModeUpdating, OpenTextModeWriting, OpenTextModeReading]
OpenBinaryModeUpdating = Literal[
    "rb+",
    "r+b",
    "+rb",
    "br+",
    "b+r",
    "+br",
    "wb+",
    "w+b",
    "+wb",
    "bw+",
    "b+w",
    "+bw",
    "ab+",
    "a+b",
    "+ab",
    "ba+",
    "b+a",
    "+ba",
    "xb+",
    "x+b",
    "+xb",
    "bx+",
    "b+x",
    "+bx",
]
OpenBinaryModeWriting = Literal["wb", "bw", "ab", "ba", "xb", "bx"]
OpenBinaryModeReading = Literal["rb", "br"]
OpenBinaryMode = Union[OpenBinaryModeUpdating, OpenBinaryModeReading, OpenBinaryModeWriting]

OpenMode = Union[OpenTextMode, OpenBinaryMode]
