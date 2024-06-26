from fastapi import Query
from typing_extensions import Annotated

from melody.kit.core import config, database, v1
from melody.kit.dependencies.common import LimitDependency, OffsetDependency
from melody.kit.dependencies.request_urls import RequestURLDependency
from melody.kit.dependencies.types import TypesDependency
from melody.kit.enums import EntityType, Tag
from melody.kit.models.pagination import Pagination
from melody.kit.models.search import (
    Search,
    SearchAlbums,
    SearchArtists,
    SearchData,
    SearchPlaylists,
    SearchTracks,
    SearchUsers,
)
from melody.kit.tokens.dependencies import TokenDependency

__all__ = ("search_entities",)


NOT_FOUND = "can not find the user with ID `{}`"
not_found = NOT_FOUND.format

QueryDependency = Annotated[str, Query()]


@v1.get(
    "/search",
    tags=[Tag.SEARCH],
    summary="Searches for entities.",
)
async def search_entities(
    query: QueryDependency,
    types: TypesDependency,
    request_url: RequestURLDependency,
    context: TokenDependency,
    offset: OffsetDependency = config.offset.default,
    limit: LimitDependency = config.limit.default,
) -> SearchData:
    albums = []
    artists = []
    playlists = []
    tracks = []
    users = []

    if EntityType.ALBUM in types:
        albums = await database.search_albums(query=query, offset=offset, limit=limit)

    if EntityType.ARTIST in types:
        artists = await database.search_artists(query=query, offset=offset, limit=limit)

    if EntityType.PLAYLIST in types:
        playlists = await database.search_playlists(query=query, offset=offset, limit=limit)

    if EntityType.TRACK in types:
        tracks = await database.search_tracks(query=query, offset=offset, limit=limit)

    if EntityType.USER in types:
        users = await database.search_users(query=query, offset=offset, limit=limit)

    search_albums = SearchAlbums(
        items=albums,
        pagination=Pagination.paginate(
            url=request_url, offset=offset, limit=limit, count=len(albums)
        ),
    )

    search_artists = SearchArtists(
        items=artists,
        pagination=Pagination.paginate(
            url=request_url, offset=offset, limit=limit, count=len(artists)
        ),
    )

    search_playlists = SearchPlaylists(
        items=playlists,
        pagination=Pagination.paginate(
            url=request_url, offset=offset, limit=limit, count=len(playlists)
        ),
    )

    search_tracks = SearchTracks(
        items=tracks,
        pagination=Pagination.paginate(
            url=request_url, offset=offset, limit=limit, count=len(tracks)
        ),
    )

    search_users = SearchUsers(
        items=users,
        pagination=Pagination.paginate(
            url=request_url, offset=offset, limit=limit, count=len(users)
        ),
    )

    search = Search(
        albums=search_albums,
        artists=search_artists,
        playlists=search_playlists,
        tracks=search_tracks,
        users=search_users,
    )

    return search.into_data()
