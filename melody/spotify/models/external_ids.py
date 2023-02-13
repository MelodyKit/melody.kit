from typing import Type, TypeVar

from attrs import define

from melody.shared.converter import CONVERTER
from melody.spotify.models.base import Base, BaseData

__all__ = ("ExternalIDs", "ExternalIDsData")


class ExternalIDsData(BaseData):
    isrc: str
    ean: str
    upc: str


E = TypeVar("E", bound="ExternalIDs")


@define()
class ExternalIDs(Base):
    isrc: str
    ean: str
    upc: str

    @classmethod
    def from_data(cls: Type[E], data: ExternalIDsData) -> E:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> ExternalIDsData:
        return CONVERTER.unstructure(self)  # type: ignore
