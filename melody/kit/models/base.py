from uuid import UUID

from attrs import define
from edgedb import Object
from typing_extensions import Self

from melody.shared.converter import CONVERTER
from melody.shared.typing import Data

__all__ = ("Base", "BaseData")


class BaseData(Data):
    id: str


@define(kw_only=True)
class Base:
    id: UUID

    @classmethod
    def from_object(cls, object: Object) -> Self:
        return cls(id=object.id)

    @classmethod
    def from_data(cls, data: BaseData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> BaseData:
        return CONVERTER.unstructure(self)  # type: ignore
