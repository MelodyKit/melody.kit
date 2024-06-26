from uuid import UUID

from fastapi import Depends
from fastapi.responses import FileResponse

from melody.kit.code import generate_code_for_uri
from melody.kit.core import config, database, v1
from melody.kit.dependencies.common import LimitDependency, OffsetDependency
from melody.kit.dependencies.request_urls import RequestURLDependency
from melody.kit.enums import EntityType, Tag
from melody.kit.errors.albums import AlbumNotFound
from melody.kit.models.album import AlbumData, AlbumTracks, AlbumTracksData
from melody.kit.models.pagination import Pagination
from melody.kit.tokens.dependencies import token_dependency
from melody.kit.uri import URI

__all__ = ("get_album", "get_album_link", "get_album_tracks")


@v1.get(
    "/albums/{album_id}",
    tags=[Tag.ALBUMS],
    summary="Fetches the album.",
    dependencies=[Depends(token_dependency)],
)
async def get_album(album_id: UUID) -> AlbumData:
    album = await database.query_album(album_id=album_id)

    if album is None:
        raise AlbumNotFound(album_id)

    return album.into_data()


@v1.get(
    "/albums/{album_id}/link",
    tags=[Tag.ALBUMS],
    summary="Fetches the album's link.",
    dependencies=[Depends(token_dependency)],
)
async def get_album_link(album_id: UUID) -> FileResponse:
    uri = URI(type=EntityType.ALBUM, id=album_id)

    path = await generate_code_for_uri(uri)

    return FileResponse(path)


@v1.get(
    "/albums/{album_id}/tracks",
    tags=[Tag.ALBUMS],
    summary="Fetches the album's tracks.",
    dependencies=[Depends(token_dependency)],
)
async def get_album_tracks(
    album_id: UUID,
    request_url: RequestURLDependency,
    offset: OffsetDependency = config.offset.default,
    limit: LimitDependency = config.limit.default,
) -> AlbumTracksData:
    counted = await database.query_album_tracks(album_id=album_id, offset=offset, limit=limit)

    if counted is None:
        raise AlbumNotFound(album_id)

    items, count = counted

    album_tracks = AlbumTracks(
        items, Pagination.paginate(url=request_url, offset=offset, limit=limit, count=count)
    )

    return album_tracks.into_data()
