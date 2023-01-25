from pathlib import Path
from uuid import UUID

__all__ = (
    # root
    "MELODY_ROOT",
    "KIT_ROOT",
    # empty
    "EMPTY",
    "EMPTY_BYTES",
    # me
    "ME",
    # space
    "SPACE",
    # v1
    "V1",
    "VERSION_1",
    # verify tokens
    "VERIFICATION_TOKEN_SIZE",
    # config
    "DEFAULT_IGNORE_SENSITIVE",
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

KIT_ROOT = Path(__file__).parent
MELODY_ROOT = KIT_ROOT.parent

EMPTY_BYTES = bytes()
EMPTY = str()

SPACE = " "

VERIFICATION_TOKEN_SIZE = 32

VERSION_1 = "1.0.0"
V1 = "/api/v1"

ME = "@me"

# defaults

DEFAULT_IGNORE_SENSITIVE = False

DEFAULT_ENCODING = "utf-8"
DEFAULT_ERRORS = "strict"

DEFAULT_COUNT = 0
DEFAULT_EXPLICIT = False
DEFAULT_ID = UUID(int=0)
DEFAULT_NAME = "unknown"
