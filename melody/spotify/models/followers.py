from typing import Type, TypeVar

from attrs import define

from melody.shared.converter import CONVERTER
from melody.spotify.models.base import Base, BaseData

__all__ = ("Followers", "FollowersData")


class FollowersData(BaseData):
    total: int


F = TypeVar("F", bound="Followers")


@define()
class Followers(Base):
    total: int

    @classmethod
    def from_data(cls: Type[F], data: FollowersData) -> F:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> FollowersData:
        return CONVERTER.unstructure(self)  # type: ignore
