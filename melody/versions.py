from versions.meta import python_version_info
from versions.versioned import get_version

import melody

__all__ = ("python_version_info", "version_info")

version_info = get_version(melody)  # type: ignore
