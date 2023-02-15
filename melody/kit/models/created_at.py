from typing import Type, TypeVar, overload

from attrs import define, field
from edgedb import Object  # type: ignore
from pendulum import DateTime

from melody.kit.models.base import Base, BaseData
from melody.shared.converter import CONVERTER
from melody.shared.date_time import convert_standard_date_time, utc_now

__all__ = (
    "CreatedAt",
    "CreatedAtData",
    "created_at_from_object",
    "created_at_from_data",
    "created_at_into_data",
)


class CreatedAtData(BaseData):
    created_at: str


C = TypeVar("C", bound="CreatedAt")


class CreatedAt(Base):
    created_at: DateTime = field(factory=utc_now)

    @classmethod
    def from_object(cls: Type[C], object: Object) -> C:  # type: ignore
        return cls(id=object.id, created_at=convert_standard_date_time(object.created_at))

    @classmethod
    def from_data(cls: Type[C], data: CreatedAtData) -> C:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> CreatedAtData:
        return CONVERTER.unstructure(self)


@overload
def created_at_from_object(object: Object) -> CreatedAt:
    ...


@overload
def created_at_from_object(object: Object, created_at_type: Type[C]) -> C:
    ...


def created_at_from_object(
    object: Object, created_at_type: Type[CreatedAt] = CreatedAt
) -> CreatedAt:
    return created_at_type.from_object(object)


@overload
def created_at_from_data(data: CreatedAtData) -> CreatedAt:
    ...


@overload
def created_at_from_data(data: CreatedAtData, created_at_type: Type[C]) -> C:
    ...


def created_at_from_data(
    data: CreatedAtData, created_at_type: Type[CreatedAt] = CreatedAt
) -> CreatedAt:
    return created_at_type.from_data(data)


def created_at_into_data(created_at: CreatedAt) -> CreatedAtData:
    return created_at.into_data()
