from typing import Type, TypeVar, overload

from attrs import define, field
from edgedb import Object  # type: ignore
from pendulum import DateTime

from melody.kit.constants import DEFAULT_DURATION
from melody.kit.models.base_stream import BaseStream, BaseStreamData
from melody.kit.models.user import User, UserData, user_from_object
from melody.shared.converter import CONVERTER
from melody.shared.date_time import convert_standard_date_time, utc_now

__all__ = (
    "TrackStream",
    "TrackStreamData",
    "track_stream_from_object",
    "track_stream_from_data",
    "track_stream_into_data",
)


class TrackStreamData(BaseStreamData):
    user: UserData


T = TypeVar("T", bound="TrackStream")


@define()
class TrackStream(BaseStream):
    user: User = field()
    created_at: DateTime = field(factory=utc_now)
    duration_ms: int = field(default=DEFAULT_DURATION)

    @classmethod
    def from_object(cls: Type[T], object: Object) -> T:  # type: ignore
        return cls(
            id=object.id,
            user=user_from_object(object.user),
            created_at=convert_standard_date_time(object.created_at),
            duration_ms=object.duration_ms,
        )

    @classmethod
    def from_data(cls: Type[T], data: TrackStreamData) -> T:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> TrackStreamData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def track_stream_from_object(object: Object) -> TrackStream:
    ...


@overload
def track_stream_from_object(object: Object, track_stream_type: Type[T]) -> T:
    ...


def track_stream_from_object(
    object: Object, track_stream_type: Type[TrackStream] = TrackStream
) -> TrackStream:
    return track_stream_type.from_object(object)


@overload
def track_stream_from_data(data: TrackStreamData) -> TrackStream:
    ...


@overload
def track_stream_from_data(data: TrackStreamData, track_stream_type: Type[T]) -> T:
    ...


def track_stream_from_data(
    data: TrackStreamData, track_stream_type: Type[TrackStream] = TrackStream
) -> TrackStream:
    return track_stream_type.from_data(data)


def track_stream_into_data(track_stream: TrackStream) -> TrackStreamData:
    return track_stream.into_data()
