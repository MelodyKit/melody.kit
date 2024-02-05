from typing import Optional, Set
from uuid import UUID

from fastapi import Depends, Query
from iters.iters import iter
from yarl import URL

from melody.kit.constants import (
    DEFAULT_LIMIT,
    DEFAULT_OFFSET,
    MAX_LIMIT,
    MIN_LIMIT,
    MIN_OFFSET,
)
from melody.kit.core import database, v1
from melody.kit.dependencies import request_url_dependency, types_dependency
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
from melody.kit.oauth2 import optional_token_dependency
from melody.kit.privacy import (
    create_playlist_accessible_predicate,
    create_user_accessible_predicate,
)

__all__ = ("search_items",)


NOT_FOUND = "can not find the user with ID `{}`"
not_found = NOT_FOUND.format


@v1.get(
    "/search",
    tags=[Tag.SEARCH],
    summary="Searches for items.",
)
async def search_items(
    query: str = Query(),
    types: Set[EntityType] = Depends(types_dependency),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    url: URL = Depends(request_url_dependency),
    self_id: Optional[UUID] = Depends(optional_token_dependency),
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
        all_playlists = await database.search_playlists(query=query, offset=offset, limit=limit)

        is_playlist_accessible = await create_playlist_accessible_predicate(self_id)

        playlists = iter(all_playlists).filter(is_playlist_accessible).list()

    if EntityType.TRACK in types:
        tracks = await database.search_tracks(query=query, offset=offset, limit=limit)

    if EntityType.USER in types:
        all_users = await database.search_users(query=query, offset=offset, limit=limit)

        is_user_accessible = await create_user_accessible_predicate(self_id)

        users = iter(all_users).filter(is_user_accessible).list()

    search_albums = SearchAlbums(
        items=albums,
        pagination=Pagination.paginate(url=url, offset=offset, limit=limit, count=len(albums)),
    )

    search_artists = SearchArtists(
        items=artists,
        pagination=Pagination.paginate(url=url, offset=offset, limit=limit, count=len(artists)),
    )

    search_playlists = SearchPlaylists(
        items=playlists,
        pagination=Pagination.paginate(url=url, offset=offset, limit=limit, count=len(playlists)),
    )

    search_tracks = SearchTracks(
        items=tracks,
        pagination=Pagination.paginate(url=url, offset=offset, limit=limit, count=len(tracks)),
    )

    search_users = SearchUsers(
        items=users,
        pagination=Pagination.paginate(url=url, offset=offset, limit=limit, count=len(users)),
    )

    search = Search(
        albums=search_albums,
        artists=search_artists,
        playlists=search_playlists,
        tracks=search_tracks,
        users=search_users,
    )

    return search.into_data()
