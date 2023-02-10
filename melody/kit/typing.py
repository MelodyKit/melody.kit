from typing import Dict, TypeVar
from uuid import UUID

__all__ = ("UUIDDict",)

T = TypeVar("T")

UUIDDict = Dict[UUID, T]
