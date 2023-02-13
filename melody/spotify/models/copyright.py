from typing import Type, TypeVar

from attrs import define

from melody.shared.converter import CONVERTER
from melody.spotify.enums import CopyrightType
from melody.spotify.models.base import Base, BaseData

__all__ = ("Copyright", "CopyrightData")


class CopyrightData(BaseData):
    text: str
    type: str


C = TypeVar("C", bound="Copyright")


@define()
class Copyright(Base):
    text: str
    type: CopyrightType

    @classmethod
    def from_data(cls: Type[C], data: CopyrightData) -> C:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> CopyrightData:
        return CONVERTER.unstructure(self)  # type: ignore
