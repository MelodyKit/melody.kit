from attrs import define, field
from edgedb import Object
from pendulum import DateTime
from typing_extensions import Self

from melody.kit.models.base import Base, BaseData
from melody.shared.converter import CONVERTER
from melody.shared.date_time import convert_standard_date_time, utc_now

__all__ = ("CreatedAt", "CreatedAtData")


class CreatedAtData(BaseData):
    created_at: str


@define()
class CreatedAt(Base):
    created_at: DateTime = field(factory=utc_now)

    @classmethod
    def from_object(cls, object: Object) -> Self:
        return cls(id=object.id, created_at=convert_standard_date_time(object.created_at))

    @classmethod
    def from_data(cls, data: CreatedAtData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> CreatedAtData:
        return CONVERTER.unstructure(self)  # type: ignore
