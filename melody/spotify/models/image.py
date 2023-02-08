from typing import Type, TypeVar

from attrs import define

from melody.shared.converter import CONVERTER
from melody.spotify.models.base import Base, BaseData


class ImageData(BaseData):
    url: str
    width: int
    height: int


I = TypeVar("I", bound="Image")


@define()
class Image(Base):
    url: str
    width: int
    height: int

    @classmethod
    def from_data(cls: Type[I], data: ImageData) -> I:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> ImageData:
        return CONVERTER.unstructure(self)  # type: ignore
