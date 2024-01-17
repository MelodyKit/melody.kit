from attrs import define
from typing_extensions import Self

from melody.shared.converter import CONVERTER
from melody.shared.typing import Data

__all__ = ("Base", "BaseData")


class BaseData(Data):
    pass


@define()
class Base:
    @classmethod
    def from_data(cls, data: BaseData) -> Self:
        return CONVERTER.structure(data, cls)

    def to_data(self) -> BaseData:
        return CONVERTER.unstructure(self)  # type: ignore
