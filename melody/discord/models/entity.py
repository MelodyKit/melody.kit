from attrs import define
from typing_extensions import Self

from melody.discord.models.base import Base, BaseData
from melody.shared.converter import CONVERTER


class EntityData(BaseData):
    id: str


@define()
class Entity(Base):
    id: str

    @classmethod
    def from_data(cls, data: EntityData) -> Self:  # type: ignore[override]
        return CONVERTER.structure(data, cls)

    def to_data(self) -> EntityData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]
