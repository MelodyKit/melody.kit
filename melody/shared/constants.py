from pathlib import Path

from colors import Color
from typing_extensions import Literal

__all__ = (
    # paths
    "HOME",
    "ROOT",
    # constants
    "EMPTY",
    "EMPTY_BYTES",
    "SPACE",
    "STAR",
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
    "WRITE_BINARY",
    # tokens
    "TOKEN",
    "VERIFICATION_TOKEN",
    # grant types
    "CLIENT_CREDENTIALS",
    "AUTHORIZATION_CODE",
    "REFRESH_TOKEN",
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

# user agent names

NAME = "MelodyKit"
PYTHON = "Python"

# image types

IMAGE_CONTENT_TYPE = "image/png"
IMAGE_TYPE = "png"

# file modes

WRITE_BINARY: Literal["wb"] = "wb"

# tokens

TOKEN: Literal["token"] = "token"
VERIFICATION_TOKEN: Literal["verification_token"] = "verification_token"

# grant types

CLIENT_CREDENTIALS = "client_credentials"
AUTHORIZATION_CODE = "authorization_code"

REFRESH_TOKEN = "refresh_token"

# response types

CODE = "code"

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
