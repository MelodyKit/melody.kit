from typing import Optional, Set
from uuid import UUID

from fastapi import Depends, Query

from melody.kit.constants import (
    DEFAULT_LIMIT,
    DEFAULT_OFFSET,
    MAX_LIMIT,
    MIN_LIMIT,
    MIN_OFFSET,
)
from melody.kit.core import database, v1
from melody.kit.dependencies import optional_access_token_dependency, types_dependency
from melody.kit.enums import EntityType
from melody.kit.models.search import Search, SearchData
from melody.kit.tags import SEARCH

__all__ = ("search_items",)


@v1.get(
    "/search",
    tags=[SEARCH],
    summary="Searches for items with the given query.",
)
async def search_items(
    query: str = Query(),
    types: Set[EntityType] = Depends(types_dependency),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    user_id_option: Optional[UUID] = Depends(optional_access_token_dependency),
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

    if EntityType.TRACK in types:
        tracks = await database.search_tracks(query=query, offset=offset, limit=limit)

    if EntityType.USER in types:
        users = await database.search_users(query=query, offset=offset, limit=limit)

    search = Search(albums=albums, artists=artists, playlists=playlists, tracks=tracks, users=users)

    return search.into_data()
