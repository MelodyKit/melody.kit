from fastapi import File, Query, UploadFile
from typing_extensions import Annotated

from melody.kit.core import config

__all__ = ("OffsetDependency", "LimitDependency", "FileDependency")

OffsetDependency = Annotated[int, Query(ge=config.offset.min)]
LimitDependency = Annotated[int, Query(ge=config.limit.min, le=config.limit.max)]

FileDependency = Annotated[UploadFile, File()]
