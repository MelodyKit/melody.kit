from attrs import define
from typing_extensions import Self

from melody.shared.converter import CONVERTER
from melody.spotify.models.base import Base, BaseData

__all__ = ("ExternalURLs", "ExternalURLsData")


class ExternalURLsData(BaseData):
    spotify: str


@define()
class ExternalURLs(Base):
    spotify: str

    @classmethod
    def from_data(cls, data: ExternalURLsData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> ExternalURLsData:
        return CONVERTER.unstructure(self)  # type: ignore
