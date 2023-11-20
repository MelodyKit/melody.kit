from typing import Type
from typing import TypedDict as Data
from typing import TypeVar, overload
from uuid import UUID

from attrs import define
from edgedb import Object  # type: ignore

from melody.shared.converter import CONVERTER

__all__ = ("Base", "BaseData", "base_from_object", "base_from_data", "base_into_data")


class BaseData(Data):
    id: str


B = TypeVar("B", bound="Base")


@define()
class Base:
    id: UUID

    @classmethod
    def from_object(cls: Type[B], object: Object) -> B:  # type: ignore
        return cls(id=object.id)

    @classmethod
    def from_data(cls: Type[B], data: BaseData) -> B:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> BaseData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def base_from_object(object: Object) -> Base:  # type: ignore
    ...


@overload
def base_from_object(object: Object, base_type: Type[B]) -> B:  # type: ignore
    ...


def base_from_object(object: Object, base_type: Type[Base] = Base) -> Base:  # type: ignore
    return base_type.from_object(object)


@overload
def base_from_data(data: BaseData) -> Base:
    ...


@overload
def base_from_data(data: BaseData, base_type: Type[B]) -> B:
    ...


def base_from_data(data: BaseData, base_type: Type[Base] = Base) -> Base:
    return base_type.from_data(data)


def base_into_data(base: Base) -> BaseData:
    return base.into_data()
