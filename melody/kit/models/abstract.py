from typing import Type, TypeVar
from uuid import UUID

from attrs import define
from edgedb import Object  # type: ignore
from typing_extensions import TypedDict as Data

__all__ = ("Abstract", "AbstractData", "abstract_from_object", "abstract_into_data")


class AbstractData(Data):
    id: str


AB = TypeVar("AB", bound="Abstract")


@define()
class Abstract:
    id: UUID

    @classmethod
    def from_object(cls: Type[AB], object: Object) -> AB:  # type: ignore
        return cls(id=object.id)

    def into_data(self) -> AbstractData:
        return AbstractData(id=str(self.id))


def abstract_from_object(object: Object) -> Abstract:
    return Abstract.from_object(object)


def abstract_into_data(abstract: Abstract) -> AbstractData:
    return abstract.into_data()
