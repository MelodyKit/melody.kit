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
    # grant types
    "CLIENT_CREDENTIALS",
    "AUTHORIZATION_CODE",
    "REFRESH_TOKEN",
    # response types
    "CODE",
    # names
    "NAME",
    "PYTHON",
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

CLIENT_CREDENTIALS = "client_credentials"
AUTHORIZATION_CODE = "authorization_code"

REFRESH_TOKEN = "refresh_token"

CODE = "code"

# defaults

DEFAULT_RETRIES = 3

DEFAULT_ENCODING = "utf-8"
DEFAULT_ERRORS = "strict"
