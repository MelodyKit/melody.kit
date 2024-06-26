from __future__ import annotations

from typing import ClassVar, List, Optional

from attrs import Factory, define
from edgedb import Object
from typing_extensions import Self
from yarl import URL

from melody.kit.config.core import CONFIG
from melody.kit.constants import DEFAULT_COUNT, DEFAULT_DURATION
from melody.kit.enums import EntityType, PrivacyType
from melody.kit.links import (
    Linked,
    apple_music_playlist,
    self_playlist,
    spotify_playlist,
    yandex_music_playlist,
)
from melody.kit.models.entity import Entity, EntityData
from melody.kit.models.pagination import Pagination, PaginationData
from melody.kit.uri import Locatable
from melody.shared.converter import CONVERTER
from melody.shared.typing import Data

__all__ = (
    # playlists
    "Playlist",
    "PlaylistData",
    # playlist tracks
    "PlaylistTracks",
    "PlaylistTracksData",
)


class PlaylistData(EntityData):
    owner: Optional[UserData]

    follower_count: int

    description: Optional[str]

    duration_ms: int

    track_count: int

    privacy_type: str


OWNER_NOT_ATTACHED = "`owner` is not attached"


@define(kw_only=True)
class Playlist(Linked, Locatable, Entity):
    TYPE: ClassVar[EntityType] = EntityType.PLAYLIST

    owner: Optional[User] = None

    follower_count: int = DEFAULT_COUNT

    description: Optional[str] = None

    duration_ms: int = DEFAULT_DURATION

    track_count: int = DEFAULT_COUNT

    privacy_type: PrivacyType = PrivacyType.DEFAULT

    def attach_owner(self, owner: User) -> Self:
        self.owner = owner

        return self

    def detach_owner(self) -> Self:
        self.owner = None

        return self

    @property
    def required_owner(self) -> User:
        owner = self.owner

        if owner is None:
            raise ValueError(OWNER_NOT_ATTACHED)

        return owner

    @classmethod
    def from_object(cls, object: Object) -> Self:
        self = super().from_object(object)

        try:
            owner_object = object.owner

        except AttributeError:
            owner = None

        else:
            owner = User.from_object(owner_object)

        self.owner = owner

        self.follower_count = object.follower_count

        self.description = object.description

        self.duration_ms = object.duration_ms

        self.track_count = object.track_count

        self.privacy_type = PrivacyType(object.privacy_type.value)

        return self

    @classmethod
    def from_data(cls, data: PlaylistData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> PlaylistData:
        return CONVERTER.unstructure(self)  # type: ignore

    @property
    def spotify_url(self) -> Optional[URL]:
        spotify_id = self.spotify_id

        return None if spotify_id is None else URL(spotify_playlist(id=spotify_id))

    @property
    def apple_music_url(self) -> Optional[URL]:
        apple_music_id = self.apple_music_id

        return None if apple_music_id is None else URL(apple_music_playlist(id=apple_music_id))

    @property
    def yandex_music_url(self) -> Optional[URL]:
        owner = self.owner

        if owner is None:
            return None

        yandex_music_id = self.yandex_music_id
        yandex_music_owner_id = owner.yandex_music_id

        return (
            None
            if yandex_music_id is None or yandex_music_owner_id is None
            else URL(yandex_music_playlist(user_id=yandex_music_owner_id, id=yandex_music_id))
        )

    @property
    def url(self) -> URL:
        return URL(self_playlist(config=CONFIG, id=self.id))


from melody.kit.models.tracks import PositionTrack, PositionTrackData
from melody.kit.models.user import User, UserData


class PlaylistTracksData(Data):
    items: List[PositionTrackData]
    pagination: PaginationData


@define()
class PlaylistTracks:
    items: List[PositionTrack] = Factory(list)
    pagination: Pagination = Factory(Pagination)

    @classmethod
    def from_data(cls, data: PlaylistTracksData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> PlaylistTracksData:
        return CONVERTER.unstructure(self)  # type: ignore
