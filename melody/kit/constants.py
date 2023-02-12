from pathlib import Path

__all__ = (
    # root
    "MELODY_ROOT",
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
)

# constants

KIT_ROOT = Path(__file__).parent
MELODY_ROOT = KIT_ROOT.parent

VERSION_1 = "1.0.0"
V1 = "/api/v1"

# defaults

DEFAULT_IGNORE_SENSITIVE = False

DEFAULT_COUNT = 0
DEFAULT_DURATION = 0
DEFAULT_EXPLICIT = False
