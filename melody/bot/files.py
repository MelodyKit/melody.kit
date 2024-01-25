from pathlib import Path
from typing import Optional, Tuple

from discord import File
from yarl import URL

from melody.bot.utils import attachment

__all__ = ("at_path",)


def at_path(path: Path) -> Optional[Tuple[File, URL]]:
    if not path.exists():
        return None

    name = path.name

    url = URL(attachment(name))

    file = File(path, name)

    return (file, url)
