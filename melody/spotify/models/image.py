from attrs import define
from typing_extensions import Self

from melody.shared.converter import CONVERTER
from melody.spotify.models.base import Base, BaseData


class ImageData(BaseData):
    url: str
    width: int
    height: int


@define()
class Image(Base):
    url: str
    width: int
    height: int

    @classmethod
    def from_data(cls, data: ImageData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> ImageData:
        return CONVERTER.unstructure(self)  # type: ignore
