from typing import Type, TypeVar

from attrs import define
from edgedb import Object  # type: ignore
from typing_extensions import TypedDict as Data

from melody.kit.constants import DEFAULT_COUNT

__all__ = ("Statistics", "StatisticsData", "statistics_from_object", "statistics_into_data")


class StatisticsData(Data):
    track_count: int
    artist_count: int
    album_count: int
    playlist_count: int
    user_count: int
    stream_count: int


S = TypeVar("S", bound="Statistics")


@define()
class Statistics:
    track_count: int = DEFAULT_COUNT
    artist_count: int = DEFAULT_COUNT
    album_count: int = DEFAULT_COUNT
    playlist_count: int = DEFAULT_COUNT
    user_count: int = DEFAULT_COUNT
    stream_count: int = DEFAULT_COUNT

    @classmethod
    def from_object(cls: Type[S], object: Object) -> S:  # type: ignore
        return cls(
            track_count=object.track_count,
            artist_count=object.artist_count,
            album_count=object.album_count,
            playlist_count=object.playlist_count,
            user_count=object.user_count,
            stream_count=object.stream_count,
        )

    def into_data(self) -> StatisticsData:
        return StatisticsData(
            track_count=self.track_count,
            artist_count=self.artist_count,
            album_count=self.album_count,
            playlist_count=self.playlist_count,
            user_count=self.user_count,
            stream_count=self.stream_count,
        )


def statistics_from_object(object: Object) -> Statistics:
    return Statistics.from_object(object)


def statistics_into_data(statistics: Statistics) -> StatisticsData:
    return statistics.into_data()
