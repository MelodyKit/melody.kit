from uuid import UUID

__all__ = (
    # main
    "DEFAULT_HOST",
    "DEFAULT_PORT",
    # models
    "DEFAULT_COUNT",
    "DEFAULT_EXPLICIT",
    "DEFAULT_ID",
    "DEFAULT_NAME",
)

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000

DEFAULT_COUNT = 0
DEFAULT_EXPLICIT = False
DEFAULT_ID = UUID(int=0)
DEFAULT_NAME = "unknown"
