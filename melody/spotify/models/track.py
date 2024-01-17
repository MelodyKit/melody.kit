from typing import List, Optional

from attrs import define
from cattrs.gen import override
from typing_extensions import Self

from melody.shared.converter import (
    CONVERTER,
    register_structure_hook,
    register_unstructure_hook,
    register_unstructure_hook_omit_client,
)
from melody.spotify.models.album import Album, AlbumData
from melody.spotify.models.artist import Artist, ArtistData
from melody.spotify.models.external_ids import ExternalIDs, ExternalIDsData
from melody.spotify.models.external_urls import ExternalURLs, ExternalURLsData
from melody.spotify.models.linked_from import LinkedFrom, LinkedFromData
from melody.spotify.models.named import Named, NamedData
from melody.spotify.models.restrictions import Restrictions, RestrictionsData

__all__ = ("Track", "TrackData")


class TrackData(NamedData):
    album: AlbumData
    artists: List[ArtistData]
    available_markets: List[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_ids: ExternalIDsData
    external_urls: ExternalURLsData
    is_playable: bool
    linked_from: LinkedFromData
    restrictions: RestrictionsData
    popularity: int
    preview_url: Optional[str]
    track_number: int
    is_local: bool


IS_PLAYABLE = "is_playable"
IS_LOCAL = "is_local"


register_unstructure_hook_rename = register_unstructure_hook(
    playable=override(rename=IS_PLAYABLE),
    local=override(rename=IS_LOCAL),
)

register_structure_hook_rename = register_structure_hook(
    playable=override(rename=IS_PLAYABLE),
    local=override(rename=IS_LOCAL),
)


@register_unstructure_hook_omit_client
@register_unstructure_hook_rename
@register_structure_hook_rename
@define()
class Track(Named):
    album: Album
    artists: List[Artist]
    available_markets: List[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_ids: ExternalIDs
    external_urls: ExternalURLs
    playable: bool
    linked_from: LinkedFrom
    restrictions: Restrictions
    popularity: int
    preview_url: Optional[str]
    track_number: int
    local: bool

    @classmethod
    def from_data(cls, data: TrackData) -> Self:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> TrackData:
        return CONVERTER.unstructure(self)  # type: ignore

    def is_playable(self) -> bool:
        return self.playable

    def is_local(self) -> bool:
        return self.local
