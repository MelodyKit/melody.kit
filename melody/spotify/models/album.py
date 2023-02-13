from typing import List

from attrs import define
from cattrs.gen import make_dict_unstructure_fn, override
from pendulum import Date

from melody.shared.converter import CONVERTER
from melody.spotify.enums import AlbumType, DatePrecision
from melody.spotify.models.artist import Artist, ArtistData
from melody.spotify.models.copyright import Copyright, CopyrightData
from melody.spotify.models.external_ids import ExternalIDs, ExternalIDsData
from melody.spotify.models.external_urls import ExternalURLs, ExternalURLsData
from melody.spotify.models.image import Image, ImageData
from melody.spotify.models.named import Named, NamedData
from melody.spotify.models.restrictions import Restrictions, RestrictionsData

__all__ = ("Album", "AlbumData")


class AlbumData(NamedData):
    album_type: str
    total_tracks: int
    available_markets: List[str]
    external_urls: ExternalURLsData
    images: List[ImageData]
    release_date: str
    release_date_precision: str
    restrictions: RestrictionsData
    copyrights: List[CopyrightData]
    external_ids: ExternalIDsData
    genres: List[str]
    label: str
    popularity: int
    artists: List[ArtistData]


@define()
class Album(Named):
    album_type: AlbumType
    total_tracks: int
    available_markets: List[str]
    external_urls: ExternalURLs
    images: List[Image]
    release_date: Date
    release_date_precision: DatePrecision
    restrictions: Restrictions
    copyrights: List[Copyright]
    external_ids: ExternalIDs
    genres: List[str]
    label: str
    popularity: int
    artists: List[Artist]


CONVERTER.register_unstructure_hook(
    Album, make_dict_unstructure_fn(Album, CONVERTER, client_unchecked=override(omit=True))
)
