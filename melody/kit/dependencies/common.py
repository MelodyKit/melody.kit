from fastapi import File, Query, UploadFile
from typing_extensions import Annotated

from melody.kit.constants import MAX_LIMIT, MIN_LIMIT, MIN_OFFSET

__all__ = ("OffsetDependency", "LimitDependency", "FileDependency")

OffsetDependency = Annotated[int, Query(ge=MIN_OFFSET)]
LimitDependency = Annotated[int, Query(ge=MIN_LIMIT, le=MAX_LIMIT)]

FileDependency = Annotated[UploadFile, File()]
