from uuid import UUID

__all__ = (
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

DEFAULT_IGNORE_KEY = False

DEFAULT_ENCODING = "utf-8"
DEFAULT_ERRORS = "strict"

DEFAULT_COUNT = 0
DEFAULT_EXPLICIT = False
DEFAULT_ID = UUID(int=0)
DEFAULT_NAME = "unknown"
