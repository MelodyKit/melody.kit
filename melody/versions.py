from versions.functions import parse_version
from versions.meta import python_version_info

from melody import __version__

__all__ = ("python_version_info", "version_info")

version_info = parse_version(__version__)
