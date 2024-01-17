from attrs import define
from typing_extensions import Self

from melody.shared.converter import CONVERTER
from melody.spotify.models.base import Base, BaseData

__all__ = ("Followers", "FollowersData")


class FollowersData(BaseData):
    total: int


@define()
class Followers(Base):
    total: int

    @classmethod
    def from_data(cls, data: FollowersData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> FollowersData:
        return CONVERTER.unstructure(self)  # type: ignore
