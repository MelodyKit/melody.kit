from uuid import UUID

from fastapi import Depends, Query
from fastapi.responses import FileResponse
from yarl import URL

from melody.kit.constants import (
    DEFAULT_LIMIT,
    DEFAULT_OFFSET,
    MAX_LIMIT,
    MIN_LIMIT,
    MIN_OFFSET,
)
from melody.kit.core import database, v1
from melody.kit.dependencies import url_dependency
from melody.kit.enums import EntityType
from melody.kit.errors import NotFound
from melody.kit.code import generate_code_for_uri
from melody.kit.models.artist import (
    ArtistAlbums,
    ArtistAlbumsData,
    ArtistData,
    ArtistTracks,
    ArtistTracksData,
)
from melody.kit.models.pagination import Pagination
from melody.kit.tags import ALBUMS, ARTISTS, LINKS, TRACKS
from melody.kit.uri import URI

__all__ = ("get_artist", "get_artist_link", "get_artist_tracks", "get_artist_albums")

CAN_NOT_FIND_ARTIST = "can not find the artist with ID `{}`"


@v1.get(
    "/artists/{artist_id}",
    tags=[ARTISTS],
    summary="Fetches the artist with the given ID.",
)
async def get_artist(artist_id: UUID) -> ArtistData:
    artist = await database.query_artist(artist_id=artist_id)

    if artist is None:
        raise NotFound(CAN_NOT_FIND_ARTIST.format(artist_id))

    return artist.into_data()


@v1.get(
    "/artists/{artist_id}/link",
    tags=[ARTISTS, LINKS],
    summary="Fetches the artist link with the given ID.",
)
async def get_artist_link(artist_id: UUID) -> FileResponse:
    uri = URI(type=EntityType.ARTIST, id=artist_id)

    path = await generate_code_for_uri(uri)

    return FileResponse(path)


@v1.get(
    "/artists/{artist_id}/tracks",
    tags=[ARTISTS, TRACKS],
    summary="Fetches artist tracks with the given ID.",
)
async def get_artist_tracks(
    artist_id: UUID,
    url: URL = Depends(url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> ArtistTracksData:
    counted = await database.query_artist_tracks(artist_id=artist_id, offset=offset, limit=limit)

    if counted is None:
        raise NotFound(CAN_NOT_FIND_ARTIST.format(artist_id))

    items, count = counted

    artist_tracks = ArtistTracks(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return artist_tracks.into_data()


@v1.get(
    "/artists/{artist_id}/albums",
    tags=[ARTISTS, ALBUMS],
    summary="Fetches artist albums with the given ID.",
)
async def get_artist_albums(
    artist_id: UUID,
    url: URL = Depends(url_dependency),
    offset: int = Query(default=DEFAULT_OFFSET, ge=MIN_OFFSET),
    limit: int = Query(default=DEFAULT_LIMIT, ge=MIN_LIMIT, le=MAX_LIMIT),
) -> ArtistAlbumsData:
    counted = await database.query_artist_albums(artist_id=artist_id, offset=offset, limit=limit)

    if counted is None:
        raise NotFound(CAN_NOT_FIND_ARTIST.format(artist_id))

    items, count = counted

    artist_albums = ArtistAlbums(
        items, Pagination.paginate(url=url, offset=offset, limit=limit, count=count)
    )

    return artist_albums.into_data()
