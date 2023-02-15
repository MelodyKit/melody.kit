from typing import Type, TypeVar, overload

from attrs import define, field
from edgedb import Object  # type: ignore

from melody.kit.constants import DEFAULT_DURATION
from melody.kit.models.created_at import CreatedAt, CreatedAtData
from melody.shared.converter import CONVERTER
from melody.shared.date_time import convert_standard_date_time

__all__ = (
    "BaseStream",
    "BaseStreamData",
    "base_stream_from_object",
    "base_stream_from_data",
    "base_stream_into_data",
)


class BaseStreamData(CreatedAtData):
    duration_ms: int


B = TypeVar("B", bound="BaseStream")


@define()
class BaseStream(CreatedAt):
    duration_ms: int = field(default=DEFAULT_DURATION)

    @classmethod
    def from_object(cls: Type[B], object: Object) -> B:  # type: ignore
        return cls(
            id=object.id,
            created_at=convert_standard_date_time(object.created_at),
            duration_ms=object.duration_ms,
        )

    @classmethod
    def from_data(cls: Type[B], data: BaseStreamData) -> B:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> BaseStreamData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def base_stream_from_object(object: Object) -> BaseStream:
    ...


@overload
def base_stream_from_object(object: Object, base_stream_type: Type[B]) -> B:
    ...


def base_stream_from_object(
    object: Object, base_stream_type: Type[BaseStream] = BaseStream
) -> BaseStream:
    return base_stream_type.from_object(object)


@overload
def base_stream_from_data(data: BaseStreamData) -> BaseStream:
    ...


@overload
def base_stream_from_data(data: BaseStreamData, base_stream_type: Type[B]) -> B:
    ...


def base_stream_from_data(
    data: BaseStreamData, base_stream_type: Type[BaseStream] = BaseStream
) -> BaseStream:
    return base_stream_type.from_data(data)


def base_stream_into_data(base_stream: BaseStream) -> BaseStreamData:
    return base_stream.into_data()
