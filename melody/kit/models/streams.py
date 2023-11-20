from __future__ import annotations

from typing import Type, TypeVar, overload

from attrs import define, field
from edgedb import Object  # type: ignore
from pendulum import DateTime

from melody.kit.constants import DEFAULT_DURATION
from melody.kit.models.created_at import CreatedAt, CreatedAtData
from melody.kit.models.track import Track, TrackData, track_from_object
from melody.kit.models.user import User, UserData, user_from_object
from melody.shared.converter import CONVERTER
from melody.shared.date_time import convert_standard_date_time, utc_now

__all__ = (
    # base streams
    "BaseStream",
    "BaseStreamData",
    "base_stream_from_object",
    "base_stream_from_data",
    "base_stream_into_data",
    # user streams
    "UserStream",
    "UserStreamData",
    "user_stream_from_object",
    "user_stream_from_data",
    "user_stream_into_data",
    # track streams
    "TrackStream",
    "TrackStreamData",
    "track_stream_from_object",
    "track_stream_from_data",
    "track_stream_into_data",
    # streams
    "Stream",
    "StreamData",
    "stream_from_object",
    "stream_from_data",
    "stream_into_data",
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
def base_stream_from_object(object: Object) -> BaseStream:  # type: ignore
    ...


@overload
def base_stream_from_object(object: Object, base_stream_type: Type[B]) -> B:  # type: ignore
    ...


def base_stream_from_object(
    object: Object, base_stream_type: Type[BaseStream] = BaseStream  # type: ignore
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


class UserStreamData(BaseStreamData):
    track: TrackData


U = TypeVar("U", bound="UserStream")


@define()
class UserStream(BaseStream):
    track: Track = field()
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
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def user_stream_from_object(object: Object) -> UserStream:  # type: ignore
    ...


@overload
def user_stream_from_object(object: Object, user_stream_type: Type[U]) -> U:  # type: ignore
    ...


def user_stream_from_object(
    object: Object, user_stream_type: Type[UserStream] = UserStream  # type: ignore
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
def track_stream_from_object(object: Object) -> TrackStream:  # type: ignore
    ...


@overload
def track_stream_from_object(object: Object, track_stream_type: Type[T]) -> T:  # type: ignore
    ...


def track_stream_from_object(
    object: Object, track_stream_type: Type[TrackStream] = TrackStream  # type: ignore
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
def stream_from_object(object: Object) -> Stream:  # type: ignore
    ...


@overload
def stream_from_object(object: Object, stream_type: Type[S]) -> S:  # type: ignore
    ...


def stream_from_object(
    object: Object, stream_type: Type[Stream] = Stream  # type: ignore
) -> Stream:
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
