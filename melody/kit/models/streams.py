from __future__ import annotations

from attrs import define, field
from edgedb import Object
from pendulum import DateTime
from typing_extensions import Self

from melody.kit.constants import DEFAULT_DURATION
from melody.kit.models.created_at import CreatedAt, CreatedAtData
from melody.kit.models.tracks import Track, TrackData
from melody.kit.models.user import User, UserData
from melody.shared.converter import CONVERTER
from melody.shared.date_time import convert_standard_date_time, utc_now

__all__ = (
    # base streams
    "BaseStream",
    "BaseStreamData",
    # user streams
    "UserStream",
    "UserStreamData",
    # track streams
    "TrackStream",
    "TrackStreamData",
    # streams
    "Stream",
    "StreamData",
)


class BaseStreamData(CreatedAtData):
    duration_ms: int


@define()
class BaseStream(CreatedAt):
    duration_ms: int = field(default=DEFAULT_DURATION)

    @classmethod
    def from_object(cls, object: Object) -> Self:
        return cls(
            id=object.id,
            created_at=convert_standard_date_time(object.created_at),
            duration_ms=object.duration_ms,
        )

    @classmethod
    def from_data(cls, data: BaseStreamData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> BaseStreamData:
        return CONVERTER.unstructure(self)  # type: ignore


class UserStreamData(BaseStreamData):
    track: TrackData


@define()
class UserStream(BaseStream):
    track: Track = field()
    created_at: DateTime = field(factory=utc_now)
    duration_ms: int = field(default=DEFAULT_DURATION)

    @classmethod
    def from_object(cls, object: Object) -> Self:
        return cls(
            id=object.id,
            track=Track.from_object(object.track),
            created_at=convert_standard_date_time(object.created_at),
            duration_ms=object.duration_ms,
        )

    @classmethod
    def from_data(cls, data: UserStreamData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> UserStreamData:
        return CONVERTER.unstructure(self)  # type: ignore


class TrackStreamData(BaseStreamData):
    user: UserData


@define()
class TrackStream(BaseStream):
    user: User = field()
    created_at: DateTime = field(factory=utc_now)
    duration_ms: int = field(default=DEFAULT_DURATION)

    @classmethod
    def from_object(cls, object: Object) -> Self:
        return cls(
            id=object.id,
            user=User.from_object(object.user),
            created_at=convert_standard_date_time(object.created_at),
            duration_ms=object.duration_ms,
        )

    @classmethod
    def from_data(cls, data: TrackStreamData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> TrackStreamData:
        return CONVERTER.unstructure(self)  # type: ignore


class StreamData(BaseStreamData):
    track: TrackData
    user: UserData


@define()
class Stream(BaseStream):
    track: Track = field()
    user: User = field()
    created_at: DateTime = field(factory=utc_now)
    duration_ms: int = field(default=DEFAULT_DURATION)

    @classmethod
    def from_object(cls, object: Object) -> Self:
        return cls(
            id=object.id,
            track=Track.from_object(object.track),
            user=User.from_object(object.user),
            created_at=convert_standard_date_time(object.created_at),
            duration_ms=object.duration_ms,
        )

    @classmethod
    def from_data(cls, data: StreamData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> StreamData:
        return CONVERTER.unstructure(self)  # type: ignore
