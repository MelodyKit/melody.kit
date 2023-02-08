from typing import Type, TypeVar

from attrs import define
from typing_extensions import TypedDict as Data

from melody.shared.converter import CONVERTER

__all__ = ("Base", "BaseData")


class BaseData(Data):
    pass


B = TypeVar("B", bound="Base")


@define()
class Base:
    @classmethod
    def from_data(cls: Type[B], data: BaseData) -> B:
        return CONVERTER.structure(data, cls)

    def to_data(self) -> BaseData:
        return CONVERTER.unstructure(self)  # type: ignore
