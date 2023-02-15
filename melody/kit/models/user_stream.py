from typing import Type, TypeVar, overload

from attrs import define, field
from edgedb import Object  # type: ignore

from melody.kit.models.base_stream import BaseStream, BaseStreamData
from melody.kit.models.track import Track, TrackData, track_from_object
from melody.shared.constants import DEFAULT_DURATION
from melody.shared.converter import CONVERTER
from melody.shared.date_time import convert_standard_date_time, utc_now

__all__ = (
    "UserStream",
    "UserStreamData",
    "user_stream_from_object",
    "user_stream_from_data",
    "user_stream_into_data",
)

class UserStreamData(BaseStreamData):
    track: TrackData


U = TypeVar("U", bound="UserStream")


@define()
class UserStream(BaseStream):
    track: Track
    created_at: DateTime = field(factory=utc_now)
    duration_ms: int = field(default=DEFAULT_DURATION)

    @classmethod
    def from_object(cls: Type[U], object: Object) -> U:  # type: ignore
        return cls(
            id=object.id,
            track=track_from_object(object.track),
            created_at=convert_standard_date_time(object.created_at),
            duration_ms=object.duration_ms,
        )

    @classmethod
    def from_data(cls: Type[U], data: UserStreamData) -> U:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserStreamData:
        return CONVERTER.unstructure(self)


@overload
def user_stream_from_object(object: Object) -> UserStream:
    ...


@overload
def user_stream_from_object(object: Object, user_stream_type: Type[U]) -> U:
    ...


def user_stream_from_object(
    object: Object, user_stream_type: Type[UserStream] = UserStream
) -> UserStream:
    return user_stream_type.from_object(object)


@overload
def user_stream_from_data(data: UserStreamData) -> UserStream:
    ...


@overload
def user_stream_from_data(data: UserStreamData, user_stream_type: Type[U]) -> U:
    ...


def user_stream_from_data(
    data: UserStreamData, user_stream_type: Type[UserStream] = UserStream
) -> UserStream:
    return user_stream_type.from_data(data)


def user_stream_into_data(user_stream: UserStream) -> UserStreamData:
    return user_stream.into_data()
