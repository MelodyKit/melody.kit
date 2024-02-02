from typing import List

from attrs import define, field
from typing_extensions import Self

from melody.kit.models.album import Album, AlbumData
from melody.kit.models.artist import Artist, ArtistData
from melody.kit.models.pagination import Pagination, PaginationData
from melody.kit.models.playlist import Playlist, PlaylistData
from melody.kit.models.tracks import Track, TrackData
from melody.kit.models.user import User, UserData
from melody.shared.converter import CONVERTER
from melody.shared.typing import Data

__all__ = (
    # albums
    "SearchAlbums",
    "SearchAlbumsData",
    # artists
    "SearchArtists",
    "SearchArtistsData",
    # playlists
    "SearchPlaylists",
    "SearchPlaylistsData",
    # tracks
    "SearchTracks",
    "SearchTracksData",
    # users
    "SearchUsers",
    "SearchUsersData",
    # results
    "Search",
    "SearchData",
)


class SearchAlbumsData(Data):
    items: List[AlbumData]
    pagination: PaginationData


@define()
class SearchAlbums:
    items: List[Album] = field(factory=list)
    pagination: Pagination = field(factory=Pagination)

    @classmethod
    def from_data(cls, data: SearchAlbumsData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> SearchAlbumsData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


class SearchArtistsData(Data):
    items: List[ArtistData]
    pagination: PaginationData


@define()
class SearchArtists:
    items: List[Artist] = field(factory=list)
    pagination: Pagination = field(factory=Pagination)

    @classmethod
    def from_data(cls, data: SearchArtistsData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> SearchArtistsData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


class SearchPlaylistsData(Data):
    items: List[PlaylistData]
    pagination: PaginationData


@define()
class SearchPlaylists:
    items: List[Playlist] = field(factory=list)
    pagination: Pagination = field(factory=Pagination)

    @classmethod
    def from_data(cls, data: SearchPlaylistsData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> SearchPlaylistsData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


class SearchTracksData(Data):
    items: List[TrackData]
    pagination: PaginationData


@define()
class SearchTracks:
    items: List[Track] = field(factory=list)
    pagination: Pagination = field(factory=Pagination)

    @classmethod
    def from_data(cls, data: SearchTracksData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> SearchTracksData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


class SearchUsersData(Data):
    items: List[UserData]
    pagination: PaginationData


@define()
class SearchUsers:
    items: List[User] = field(factory=list)
    pagination: Pagination = field(factory=Pagination)

    @classmethod
    def from_data(cls, data: SearchUsersData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> SearchUsersData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]


class SearchData(Data):
    albums: SearchAlbumsData
    artists: SearchArtistsData
    playlists: SearchPlaylistsData
    tracks: SearchTracksData
    users: SearchUsersData


@define(kw_only=True)
class Search:
    albums: SearchAlbums = field(factory=SearchAlbums)
    artists: SearchArtists = field(factory=SearchArtists)
    playlists: SearchPlaylists = field(factory=SearchPlaylists)
    tracks: SearchTracks = field(factory=SearchTracks)
    users: SearchUsers = field(factory=SearchUsers)

    @classmethod
    def from_data(cls, data: SearchData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> SearchData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]
