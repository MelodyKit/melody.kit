from typing_extensions import Literal

__all__ = (
    # empty
    "EMPTY",
    "EMPTY_BYTES",
    # space
    "SPACE",
    # star
    "STAR",
    # methods
    "HEAD",
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "CONNECT",
    "OPTIONS",
    "TRACE",
    # images
    "IMAGE_CONTENT_TYPE",
    "IMAGE_TYPE",
    # modes
    "WRITE_BINARY",
    # token
    "TOKEN",
    # grant types
    "CLIENT_CREDENTIALS",
    "AUTHORIZATION_CODE",
    "REFRESH_TOKEN",
    # response types
    "CODE",
    # names
    "NAME",
    "PYTHON",
    # colors
    "MELODY_PURPLE",
    "MELODY_BLUE",
    "MELODY_COLORS",
    # defaults
    "DEFAULT_RETRIES",
    "DEFAULT_ENCODING",
    "DEFAULT_ERRORS",
)

# constants

EMPTY = str()
EMPTY_BYTES = bytes()

SPACE = " "

STAR = "*"

HEAD = "HEAD"
GET = "GET"

POST = "POST"
PUT = "PUT"
PATCH = "PATCH"

DELETE = "DELETE"

CONNECT = "CONNECT"
OPTIONS = "OPTIONS"
TRACE = "TRACE"

NAME = "MelodyKit"
PYTHON = "Python"

IMAGE_CONTENT_TYPE = "image/png"
IMAGE_TYPE = "png"

WRITE_BINARY: Literal["wb"] = "wb"

TOKEN: Literal["token"] = "token"

CLIENT_CREDENTIALS = "client_credentials"
AUTHORIZATION_CODE = "authorization_code"

REFRESH_TOKEN = "refresh_token"

CODE = "code"

MELODY_PURPLE = 0xCC55FF
MELODY_BLUE = 0x55CCFF

MELODY_COLORS = (MELODY_PURPLE, MELODY_BLUE)

# defaults

DEFAULT_RETRIES = 3

DEFAULT_ENCODING = "utf-8"
DEFAULT_ERRORS = "strict"
