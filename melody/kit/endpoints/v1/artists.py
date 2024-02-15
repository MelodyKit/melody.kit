from uuid import UUID

from fastapi import Depends
from fastapi.responses import FileResponse

from melody.kit.code import generate_code_for_uri
from melody.kit.constants import DEFAULT_LIMIT, DEFAULT_OFFSET
from melody.kit.core import database, v1
from melody.kit.dependencies import LimitDependency, OffsetDependency, RequestURLDependency
from melody.kit.enums import EntityType, Tag
from melody.kit.errors import NotFound
from melody.kit.models.artist import (
    ArtistAlbums,
    ArtistAlbumsData,
    ArtistData,
    ArtistTracks,
    ArtistTracksData,
)
from melody.kit.models.pagination import Pagination
from melody.kit.oauth2 import token_dependency
from melody.kit.uri import URI

__all__ = ("get_artist", "get_artist_link", "get_artist_tracks", "get_artist_albums")

CAN_NOT_FIND_ARTIST = "can not find the artist with ID `{}`"
can_not_find_artist = CAN_NOT_FIND_ARTIST.format


@v1.get(
    "/artists/{artist_id}",
    tags=[Tag.ARTISTS],
    summary="Fetches the artist.",
    dependencies=[Depends(token_dependency)],
)
async def get_artist(artist_id: UUID) -> ArtistData:
    artist = await database.query_artist(artist_id=artist_id)

    if artist is None:
        raise NotFound(can_not_find_artist(artist_id))

    return artist.into_data()


@v1.get(
    "/artists/{artist_id}/link",
    tags=[Tag.ARTISTS],
    summary="Fetches the artist's link.",
    dependencies=[Depends(token_dependency)],
)
async def get_artist_link(artist_id: UUID) -> FileResponse:
    uri = URI(type=EntityType.ARTIST, id=artist_id)

    path = await generate_code_for_uri(uri)

    return FileResponse(path)


@v1.get(
    "/artists/{artist_id}/tracks",
    tags=[Tag.ARTISTS],
    summary="Fetches the artist's tracks.",
    dependencies=[Depends(token_dependency)],
)
async def get_artist_tracks(
    artist_id: UUID,
    request_url: RequestURLDependency,
    offset: OffsetDependency = DEFAULT_OFFSET,
    limit: LimitDependency = DEFAULT_LIMIT,
) -> ArtistTracksData:
    counted = await database.query_artist_tracks(artist_id=artist_id, offset=offset, limit=limit)

    if counted is None:
        raise NotFound(can_not_find_artist(artist_id))

    items, count = counted

    artist_tracks = ArtistTracks(
        items, Pagination.paginate(url=request_url, offset=offset, limit=limit, count=count)
    )

    return artist_tracks.into_data()


@v1.get(
    "/artists/{artist_id}/albums",
    tags=[Tag.ARTISTS],
    summary="Fetches the artist's albums.",
    dependencies=[Depends(token_dependency)],
)
async def get_artist_albums(
    artist_id: UUID,
    request_url: RequestURLDependency,
    offset: OffsetDependency = DEFAULT_OFFSET,
    limit: LimitDependency = DEFAULT_LIMIT,
) -> ArtistAlbumsData:
    counted = await database.query_artist_albums(artist_id=artist_id, offset=offset, limit=limit)

    if counted is None:
        raise NotFound(can_not_find_artist(artist_id))

    items, count = counted

    artist_albums = ArtistAlbums(
        items, Pagination.paginate(url=request_url, offset=offset, limit=limit, count=count)
    )

    return artist_albums.into_data()
