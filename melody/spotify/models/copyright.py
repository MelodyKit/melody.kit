from attrs import define
from typing_extensions import Self

from melody.shared.converter import CONVERTER
from melody.spotify.enums import CopyrightType
from melody.spotify.models.base import Base, BaseData

__all__ = ("Copyright", "CopyrightData")


class CopyrightData(BaseData):
    text: str
    type: str


@define()
class Copyright(Base):
    text: str
    type: CopyrightType

    @classmethod
    def from_data(cls, data: CopyrightData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> CopyrightData:
        return CONVERTER.unstructure(self)  # type: ignore
