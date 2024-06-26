from attrs import define
from edgedb import Object
from pendulum import DateTime
from typing_extensions import Self

from melody.kit.models.base import Base, BaseData
from melody.shared.converter import CONVERTER
from melody.shared.time import convert_standard_date_time

__all__ = ("Tracked", "TrackedData")


class TrackedData(BaseData):
    created_at: str


@define(kw_only=True)
class Tracked(Base):
    created_at: DateTime

    @classmethod
    def from_object(cls, object: Object) -> Self:
        return cls(id=object.id, created_at=convert_standard_date_time(object.created_at))

    @classmethod
    def from_data(cls, data: TrackedData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> TrackedData:
        return CONVERTER.unstructure(self)  # type: ignore
