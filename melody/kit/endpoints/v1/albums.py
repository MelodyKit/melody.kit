from uuid import UUID

from fastapi import Depends, Query
from fastapi.responses import FileResponse
from yarl import URL

from melody.kit.code import generate_code_for_uri
from melody.kit.constants import (
    DEFAULT_LIMIT,
    DEFAULT_OFFSET,
    MAX_LIMIT,
    MIN_LIMIT,
    MIN_OFFSET,
)
from melody.kit.core import database, v1
from melody.kit.dependencies import request_url_dependency
from melody.kit.enums import EntityType
from melody.kit.errors import NotFound
from melody.kit.models.album import AlbumData, AlbumTracks, AlbumTracksData
from melody.kit.models.pagination import Pagination
from melody.kit.tags import ALBUMS, LINKS, TRACKS
from melody.kit.uri import URI

__all__ = ("get_album", "get_album_link", "get_album_tracks")

CAN_NOT_FIND_ALBUM = "can not find the album with ID `{}`"
can_not_find_album = CAN_NOT_FIND_ALBUM.format


@v1.get(
    "/albums/{album_id}",
    tags=[ALBUMS],
    summary="Fetches the album with the given ID.",
)
async def get_album(album_id: UUID) -> AlbumData:
    album = await database.query_album(album_id=album_id)

    if album is None:
        raise NotFound(can_not_find_album(album_id))

    return album.into_data()


@v1.get(
    "/albums/{album_id}/link",
    tags=[ALBUMS, LINKS],
    summary="Fetches the album link with the given ID.",
)
async def get_album_link(album_id: UUID) -> FileResponse:
    uri = URI(type=EntityType.ALBUM, id=album_id)

    path = await generate_code_for_uri(uri)

    return FileResponse(path)


@v1.get(
    "/albums/{album_id}/tracks",
    tags=[ALBUMS, TRACKS],
    summary="Fetches album tracks with the given ID.",
)
async def get_album_tracks(
    album_id: UUID,
    url: URL = Depends(request_url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> AlbumTracksData:
    counted = await database.query_album_tracks(album_id=album_id, offset=offset, limit=limit)

    if counted is None:
        raise NotFound(can_not_find_album(album_id))

    items, count = counted

    album_tracks = AlbumTracks(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return album_tracks.into_data()
