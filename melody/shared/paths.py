from pathlib import Path
from typing import TypeVar

__all__ = ("Path", "expand_user", "prepare_directory")

P = TypeVar("P", bound=Path)


def expand_user(path: P) -> P:
    return path.expanduser()


def prepare_directory(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
