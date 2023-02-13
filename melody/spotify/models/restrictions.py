from typing import Type, TypeVar

from attrs import define

from melody.shared.converter import CONVERTER
from melody.spotify.enums import RestrictionsReason
from melody.spotify.models.base import Base, BaseData

__all__ = ("Restrictions", "RestrictionsData")


class RestrictionsData(BaseData):
    reason: str


R = TypeVar("R", bound="Restrictions")


@define()
class Restrictions(Base):
    reason: RestrictionsReason

    @classmethod
    def from_data(cls: Type[R], data: RestrictionsData) -> R:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> RestrictionsData:
        return CONVERTER.unstructure(self)  # type: ignore
