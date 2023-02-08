from __future__ import annotations

from typing import List, Optional, Type, TypeVar

from attrs import define, field
from edgedb import Object  # type: ignore
from pendulum import DateTime

from melody.kit.constants import DEFAULT_COUNT, DEFAULT_DURATION
from melody.kit.enums import PrivacyType, URIType
from melody.kit.models.base import Base, BaseData
from melody.kit.models.uri import URIData
from melody.kit.uri import URI
from melody.kit.utils import convert_standard_date_time, utc_now
from melody.shared.constants import EMPTY

__all__ = (
    "Playlist",
    "PlaylistData",
    "PlaylistTracks",
    "PlaylistTracksData",
    "playlist_from_object",
    "playlist_into_data",
)


class PlaylistData(URIData, BaseData):
    user: UserData

    description: str

    duration_ms: int

    track_count: int
    privacy_type: str


P = TypeVar("P", bound="Playlist")


@define()
class Playlist(Base):
    user: User = field()

    description: str = field(default=EMPTY)

    duration_ms: int = field(default=DEFAULT_DURATION)

    track_count: int = field(default=DEFAULT_COUNT)

    privacy_type: PrivacyType = field(default=PrivacyType.DEFAULT)

    created_at: DateTime = field(factory=utc_now)

    spotify_id: Optional[str] = field(default=None)
    apple_music_id: Optional[str] = field(default=None)
    yandex_music_id: Optional[str] = field(default=None)

    @classmethod
    def from_object(cls: Type[P], object: Object) -> P:  # type: ignore
        return cls(
            id=object.id,
            name=object.name,
            user=user_from_object(object.user),
            description=object.description,
            duration_ms=object.duration_ms,
            track_count=object.track_count,
            privacy_type=PrivacyType(object.privacy_type.value),
            created_at=convert_standard_date_time(object.created_at),
            spotify_id=object.spotify_id,
            apple_music_id=object.apple_music_id,
            yandex_music_id=object.yandex_music_id,
        )

    def into_data(self) -> PlaylistData:
        return PlaylistData(
            id=str(self.id),
            name=self.name,
            created_at=str(self.created_at),
            spotify_id=self.spotify_id,
            apple_music_id=self.apple_music_id,
            yandex_music_id=self.yandex_music_id,
            uri=str(self.uri),
            user=user_into_data(self.user),
            description=self.description,
            duration_ms=self.duration_ms,
            track_count=self.track_count,
            privacy_type=self.privacy_type.value,
        )

    @property
    def uri(self) -> URI:
        return URI(type=URIType.PLAYLIST, id=self.id)


def playlist_from_object(object: Object) -> Playlist:
    return Playlist.from_object(object)


def playlist_into_data(playlist: Playlist) -> PlaylistData:
    return playlist.into_data()


from melody.kit.models.track import Track, TrackData
from melody.kit.models.user import User, UserData, user_from_object, user_into_data

PlaylistTracks = List[Track]
PlaylistTracksData = List[TrackData]
