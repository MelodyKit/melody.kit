from typing import Type, TypeVar, overload

from attrs import define
from edgedb import Object  # type: ignore
from typing_extensions import TypedDict as Data

from melody.kit.constants import DEFAULT_COUNT
from melody.shared.converter import CONVERTER

__all__ = (
    "Statistics",
    "StatisticsData",
    "statistics_from_object",
    "statistics_from_data",
    "statistics_into_data",
)


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

    @classmethod
    def from_data(cls: Type[S], data: StatisticsData) -> S:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> StatisticsData:
        return CONVERTER.unstructure(self)  # type: ignore


@overload
def statistics_from_object(object: Object) -> Statistics:  # type: ignore
    ...


@overload
def statistics_from_object(object: Object, statistics_type: Type[S]) -> S:  # type: ignore
    ...


def statistics_from_object(
    object: Object, statistics_type: Type[Statistics] = Statistics  # type: ignore
) -> Statistics:
    return statistics_type.from_object(object)


@overload
def statistics_from_data(data: StatisticsData) -> Statistics:
    ...


@overload
def statistics_from_data(data: StatisticsData, statistics_type: Type[S]) -> S:
    ...


def statistics_from_data(
    data: StatisticsData, statistics_type: Type[Statistics] = Statistics
) -> Statistics:
    return statistics_type.from_data(data)


def statistics_into_data(statistics: Statistics) -> StatisticsData:
    return statistics.into_data()
