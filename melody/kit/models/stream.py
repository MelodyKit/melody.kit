from typing import Type, TypeVar, overload

from attrs import define, field
from edgedb import Object  # type: ignore
from pendulum import DateTime

from melody.kit.constants import DEFAULT_DURATION
from melody.kit.models.base_stream import BaseStream, BaseStreamData
from melody.kit.models.track import Track, TrackData, track_from_object
from melody.kit.models.user import User, UserData, user_from_object
from melody.shared.converter import CONVERTER
from melody.shared.date_time import convert_standard_date_time, utc_now

__all__ = ("Stream", "StreamData", "stream_from_object", "stream_from_data", "stream_into_data")


class StreamData(BaseStreamData):
    track: TrackData
    user: UserData


S = TypeVar("S", bound="Stream")


@define()
class Stream(BaseStream):
    track: Track = field()
    user: User = field()
    created_at: DateTime = field(factory=utc_now)
    duration_ms: int = field(default=DEFAULT_DURATION)

    @classmethod
    def from_object(cls: Type[S], object: Object) -> S:  # type: ignore
        return cls(
            id=object.id,
            track=track_from_object(object.track),
            user=user_from_object(object.user),
            created_at=convert_standard_date_time(object.created_at),
            duration_ms=object.duration_ms,
        )

    @classmethod
    def from_data(cls: Type[S], data: StreamData) -> S:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> StreamData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def stream_from_object(object: Object) -> Stream:
    ...


@overload
def stream_from_object(object: Object, stream_type: Type[S]) -> S:
    ...


def stream_from_object(object: Object, stream_type: Type[Stream] = Stream) -> Stream:
    return stream_type.from_object(object)


@overload
def stream_from_data(data: StreamData) -> Stream:
    ...


@overload
def stream_from_data(data: StreamData, stream_type: Type[S]) -> S:
    ...


def stream_from_data(data: StreamData, stream_type: Type[Stream] = Stream) -> Stream:
    return stream_type.from_data(data)


def stream_into_data(stream: Stream) -> StreamData:
    return stream.into_data()
