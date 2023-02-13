from typing import List, Optional, Type, TypeVar

from attrs import define
from cattrs.gen import make_dict_structure_fn, make_dict_unstructure_fn, override

from melody.shared.converter import CONVERTER
from melody.spotify.models.album import Album, AlbumData
from melody.spotify.models.artist import Artist, ArtistData
from melody.spotify.models.copyright import Copyright, CopyrightData
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


T = TypeVar("T", bound="Track")


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
    def from_data(cls: Type[T], data: TrackData) -> T:  # type: ignore
        return CONVERTER.structure(data, cls)

    def into_data(self) -> TrackData:
        return CONVERTER.unstructure(self)  # type: ignore

    def is_playable(self) -> bool:
        return self.playable

    def is_local(self) -> bool:
        return self.local


IS_PLAYABLE = "is_playable"
IS_LOCAL = "is_local"


CONVERTER.register_unstructure_hook(
    Track,
    make_dict_unstructure_fn(
        Track,
        CONVERTER,
        client_unchecked=override(omit=True),
        playable=override(rename=IS_PLAYABLE),
        local=override(rename=IS_LOCAL),
    )
)

CONVERTER.register_structure_hook(
    Track,
    make_dict_structure_fn(
        Track,
        CONVERTER,
        playable=override(rename=IS_PLAYABLE),
        local=override(rename=IS_LOCAL),
    )
)
