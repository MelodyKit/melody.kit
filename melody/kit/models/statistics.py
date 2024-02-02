from attrs import define
from edgedb import Object
from typing_extensions import Self

from melody.kit.constants import DEFAULT_COUNT
from melody.shared.converter import CONVERTER
from melody.shared.typing import Data

__all__ = ("Statistics", "StatisticsData")


class StatisticsData(Data):
    track_count: int
    artist_count: int
    album_count: int
    playlist_count: int
    user_count: int
    stream_count: int


@define(kw_only=True)
class Statistics:
    track_count: int = DEFAULT_COUNT
    artist_count: int = DEFAULT_COUNT
    album_count: int = DEFAULT_COUNT
    playlist_count: int = DEFAULT_COUNT
    user_count: int = DEFAULT_COUNT
    stream_count: int = DEFAULT_COUNT

    @classmethod
    def from_object(cls, object: Object) -> Self:
        return cls(
            track_count=object.track_count,
            artist_count=object.artist_count,
            album_count=object.album_count,
            playlist_count=object.playlist_count,
            user_count=object.user_count,
            stream_count=object.stream_count,
        )

    @classmethod
    def from_data(cls, data: StatisticsData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> StatisticsData:
        return CONVERTER.unstructure(self)  # type: ignore
