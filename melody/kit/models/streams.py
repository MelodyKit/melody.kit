from __future__ import annotations

from typing import Optional

from attrs import define
from edgedb import Object
from typing_extensions import Self

from melody.kit.models.tracked import Tracked, TrackedData
from melody.kit.models.tracks import Track
from melody.kit.models.user import User
from melody.shared.converter import CONVERTER
from melody.shared.date_time import convert_standard_date_time

__all__ = ("Stream", "StreamData")


class StreamData(TrackedData):
    duration_ms: int


@define(kw_only=True)
class Stream(Tracked):
    duration_ms: int

    track: Optional[Track] = None
    user: Optional[User] = None

    def attach_track(self, track: Track) -> Self:
        self.track = track

        return self

    def detach_track(self) -> Self:
        self.track = None

        return self

    def attach_user(self, user: User) -> Self:
        self.user = user

        return self

    def detach_user(self) -> Self:
        self.user = None

        return self

    @classmethod
    def from_object(cls, object: Object) -> Self:
        return cls(
            id=object.id,
            created_at=convert_standard_date_time(object.created_at),
            duration_ms=object.duration_ms,
        )

    @classmethod
    def from_data(cls, data: StreamData) -> Self:  # type: ignore[override]
        return CONVERTER.structure(data, cls)

    def into_data(self) -> StreamData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]
