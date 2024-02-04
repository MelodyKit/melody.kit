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


TRACK_NOT_ATTACHED = "`track` is not attached"
USER_NOT_ATTACHED = "`user` is not attached"


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

    @property
    def required_track(self) -> Track:
        track = self.track

        if track is None:
            raise ValueError(TRACK_NOT_ATTACHED)

        return track

    def attach_user(self, user: User) -> Self:
        self.user = user

        return self

    def detach_user(self) -> Self:
        self.user = None

        return self

    @property
    def required_user(self) -> User:
        user = self.user

        if user is None:
            raise ValueError(USER_NOT_ATTACHED)

        return user

    @classmethod
    def from_object(cls, object: Object) -> Self:
        self = cls(
            id=object.id,
            created_at=convert_standard_date_time(object.created_at),
            duration_ms=object.duration_ms,
        )

        try:
            track_object = object.track

        except AttributeError:
            track = None

        else:
            track = Track.from_object(track_object)

        self.track = track

        try:
            user_object = object.user

        except AttributeError:
            user = None

        else:
            user = User.from_object(user_object)

        self.user = user

        return self

    @classmethod
    def from_data(cls, data: StreamData) -> Self:  # type: ignore[override]
        return CONVERTER.structure(data, cls)

    def into_data(self) -> StreamData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]
