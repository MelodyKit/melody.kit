from uuid import UUID

__all__ = (
    # empty
    "EMPTY",
    "EMPTY_BYTES",
    # me
    "ME",
    # application name
    "NAME",
    # space
    "SPACE",
    # v1
    "V1",
    "VERSION_1",
    # config
    "DEFAULT_IGNORE_KEY",
    # encoding
    "DEFAULT_ENCODING",
    "DEFAULT_ERRORS",
    # models
    "DEFAULT_COUNT",
    "DEFAULT_EXPLICIT",
    "DEFAULT_ID",
    "DEFAULT_NAME",
)

# constants

EMPTY_BYTES = bytes()
EMPTY = str()

SPACE = " "

NAME = "melody.kit"
VERSION_1 = "1.0.0"
V1 = "/api/v1"

ME = "@me"

# defaults

DEFAULT_IGNORE_KEY = False

DEFAULT_ENCODING = "utf-8"
DEFAULT_ERRORS = "strict"

DEFAULT_COUNT = 0
DEFAULT_EXPLICIT = False
DEFAULT_ID = UUID(int=0)
DEFAULT_NAME = "unknown"
