from versions import parse_version, python_version_info

from melody import __version__

__all__ = ("python_version_info", "version_info")

version_info = parse_version(__version__)
