from typing import Type, TypeVar

from attrs import define

from melody.shared.converter import CONVERTER
from melody.spotify.models.base import Base, BaseData

__all__ = ("ExternalURLs", "ExternalURLsData")


class ExternalURLsData(BaseData):
    spotify: str


E = TypeVar("E", bound="ExternalURLs")


@define()
class ExternalURLs(Base):
    spotify: str

    @classmethod
    def from_data(cls: Type[E], data: ExternalURLsData) -> E:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> ExternalURLsData:
        return CONVERTER.unstructure(self)  # type: ignore
