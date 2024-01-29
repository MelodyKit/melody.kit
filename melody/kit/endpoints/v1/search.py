from typing import Optional, Set
from uuid import UUID

from fastapi import Depends, Query
from iters.iters import iter
from typing_aliases import Predicate
from yarl import URL

from melody.kit.constants import (
    DEFAULT_LIMIT,
    DEFAULT_OFFSET,
    MAX_LIMIT,
    MIN_LIMIT,
    MIN_OFFSET,
)
from melody.kit.core import database, v1
from melody.kit.dependencies import (
    optional_access_token_dependency,
    request_url_dependency,
    types_dependency,
)
from melody.kit.enums import EntityType
from melody.kit.errors import NotFound
from melody.kit.models.pagination import Pagination
from melody.kit.models.playlist import Playlist
from melody.kit.models.search import (
    Search,
    SearchAlbums,
    SearchArtists,
    SearchData,
    SearchPlaylists,
    SearchTracks,
    SearchUsers,
)
from melody.kit.privacy import friends_set, is_playlist_accessible, is_playlist_public
from melody.kit.tags import SEARCH

__all__ = ("search_items",)


def is_playlist_accessible_by(self_id: UUID, friends: Set[UUID]) -> Predicate[Playlist]:
    def is_playlist_accessible_predicate(playlist: Playlist) -> bool:
        playlist_user = playlist.user

        return is_playlist_accessible(self_id, playlist, playlist_user, playlist_user.id in friends)

    return is_playlist_accessible_predicate


NOT_FOUND = "can not find the user with ID `{}`"
not_found = NOT_FOUND.format


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
    url: URL = Depends(request_url_dependency),
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

        if user_id_option is None:
            playlists = iter(all_playlists).filter(is_playlist_public).list()

        else:
            user_id = user_id_option

            friends = await friends_set(user_id)

            if friends is None:
                raise NotFound(not_found(user_id))

            playlists = (
                iter(all_playlists).filter(is_playlist_accessible_by(user_id, friends)).list()
            )

    if EntityType.TRACK in types:
        tracks = await database.search_tracks(query=query, offset=offset, limit=limit)

    if EntityType.USER in types:
        users = await database.search_users(query=query, offset=offset, limit=limit)

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
