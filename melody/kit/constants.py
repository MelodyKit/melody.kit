from pathlib import Path

__all__ = (
    # root
    "KIT_ROOT",
    # v1
    "V1",
    "VERSION_1",
    # config
    "DEFAULT_IGNORE_SENSITIVE",
    # models
    "DEFAULT_COUNT",
    "DEFAULT_DURATION",
    "DEFAULT_EXPLICIT",
    "DEFAULT_POSITION",
)

# root

KIT_ROOT = Path(__file__).parent

# v1

VERSION_1 = "1.0.0"
V1 = "/api/v1"

# API-related

DEFAULT_OFFSET = 0
MIN_OFFSET = 0

DEFAULT_LIMIT = 100
MIN_LIMIT = 0
MAX_LIMIT = 100

# defaults

DEFAULT_IGNORE_SENSITIVE = False

DEFAULT_COUNT = 0
DEFAULT_DURATION = 0
DEFAULT_EXPLICIT = False
DEFAULT_POSITION = 0
