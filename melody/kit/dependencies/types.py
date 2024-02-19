from typing import Optional, Set

from fastapi import Depends
from iters.iters import iter
from typing_extensions import Annotated

from melody.kit.enums import EntityType
from melody.kit.errors.validation import ValidationError

__all__ = (
    # types
    "EntityTypes",
    # dependencies
    "TypesDependency",
    # dependables
    "types_dependency",
)

INVALID_TYPES = "types `{}` are invalid"
invalid_types = INVALID_TYPES.format

TYPES_SEPARATOR = ","

EntityTypes = Set[EntityType]


def split_types(types: str) -> Set[str]:
    if not types:
        return set()  # types empty -> default to none

    return set(types.split(TYPES_SEPARATOR))


def types_dependency(types: Optional[str] = None) -> EntityTypes:
    if types is None:  # types not provided -> default to all
        return set(EntityType)

    try:
        return iter(split_types(types)).map(EntityType).set()

    except ValueError:
        raise ValidationError(invalid_types(types)) from None


TypesDependency = Annotated[EntityTypes, Depends(types_dependency)]
