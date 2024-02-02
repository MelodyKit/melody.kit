from pathlib import Path
from typing import Literal

from colors import Color

__all__ = (
    # paths
    "HOME",
    "ROOT",
    # constants
    "EMPTY",
    "EMPTY_BYTES",
    "SPACE",
    "STAR",
    "SLASH",
    # HTTP methods
    "HEAD",
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "CONNECT",
    "OPTIONS",
    "TRACE",
    # image types
    "IMAGE_CONTENT_TYPE",
    "IMAGE_TYPE",
    # file modes
    "READ",
    "WRITE",
    "READ_BINARY",
    "WRITE_BINARY",
    # tokens
    "ACCESS_TOKEN",
    "REFRESH_TOKEN",
    "VERIFICATION_TOKEN",
    # response types
    "CODE",
    # user agent names
    "NAME",
    "PYTHON",
    # colors
    "MELODY_PURPLE",
    "MELODY_BLUE",
    "MELODY_COLORS",
    "BYTE",
    "ZERO",
    # defaults
    "DEFAULT_RETRIES",
    "DEFAULT_ENCODING",
    "DEFAULT_ERRORS",
)

# paths

HOME = Path.home()

ROOT = Path(__file__).parent.parent  # file -> shared -> root

# constants

EMPTY = str()
EMPTY_BYTES = bytes()

SPACE = " "

STAR = "*"

SLASH = "/"

# HTTP methods

HEAD = "HEAD"
GET = "GET"

POST = "POST"
PUT = "PUT"
PATCH = "PATCH"

DELETE = "DELETE"

CONNECT = "CONNECT"
OPTIONS = "OPTIONS"
TRACE = "TRACE"

# HTTP timeout

DEFAULT_TIMEOUT = 150.0

# user agent names

NAME = "MelodyKit"
PYTHON = "Python"

# image types

IMAGE_CONTENT_TYPE = "image/png"
IMAGE_TYPE = "png"

# file modes

READ: Literal["r"] = "r"
WRITE: Literal["w"] = "w"
READ_BINARY: Literal["rb"] = "rb"
WRITE_BINARY: Literal["wb"] = "wb"

# tokens

ACCESS_TOKEN: Literal["access_token"] = "access_token"
REFRESH_TOKEN: Literal["refresh_token"] = "refresh_token"
VERIFICATION_TOKEN: Literal["verification_token"] = "verification_token"

# codes

CODE = "code"
CODE_SIZE = 32
CODE_VERIFIER_SIZE = 96

# colors

MELODY_PURPLE = Color(0xCC55FF)
MELODY_BLUE = Color(0x55CCFF)

MELODY_COLORS = (MELODY_PURPLE, MELODY_BLUE)

BYTE = 0xFF
ZERO = 0x00

# defaults

DEFAULT_RETRIES = 3

DEFAULT_ENCODING = "utf-8"
DEFAULT_ERRORS = "strict"

DEFAULT_CLOSEFD = True

# redis

NAME_SEPARATOR = ":"
