from uuid import UUID

from fastapi import status
from fastapi.responses import FileResponse
from iters import iter

from melody.kit.core import database, v1
from melody.kit.enums import EntityType
from melody.kit.errors import Error, ErrorCode
from melody.kit.models.album import album_into_data
from melody.kit.models.artist import (
    ArtistAlbumsData,
    ArtistData,
    ArtistTracksData,
    artist_into_data,
)
from melody.kit.models.track import track_into_data
from melody.kit.tags import ALBUMS, ARTISTS, LINKS, TRACKS
from melody.kit.uri import URI

__all__ = ("get_artist", "get_artist_link")

CAN_NOT_FIND_ARTIST = "can not find the artist with ID `{}`"


@v1.get(
    "/artists/{artist_id}",
    tags=[ARTISTS],
    summary="Fetches the artist with the given ID.",
)
async def get_artist(artist_id: UUID) -> ArtistData:
    artist = await database.query_artist(artist_id)

    if artist is None:
        raise Error(
            CAN_NOT_FIND_ARTIST.format(artist_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return artist_into_data(artist)


@v1.get(
    "/artists/{artist_id}/link",
    tags=[ARTISTS, LINKS],
    summary="Fetches the artist link with the given ID.",
)
async def get_artist_link(artist_id: UUID) -> FileResponse:
    uri = URI(type=EntityType.ARTIST, id=artist_id)

    path = await uri.create_link()

    return FileResponse(path)


@v1.get(
    "/artists/{artist_id}/albums",
    tags=[ARTISTS, ALBUMS],
    summary="Fetches artist albums with the given ID.",
)
async def get_artist_albums(artist_id: UUID) -> ArtistAlbumsData:
    albums = await database.query_artist_albums(artist_id)

    if albums is None:
        raise Error(
            CAN_NOT_FIND_ARTIST.format(artist_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return iter(albums).map(album_into_data).list()


@v1.get(
    "/artists/{artist_id}/tracks",
    tags=[ARTISTS, TRACKS],
    summary="Fetches artist tracks with the given ID.",
)
async def get_artist_tracks(artist_id: UUID) -> ArtistTracksData:
    tracks = await database.query_artist_tracks(artist_id)

    if tracks is None:
        raise Error(
            CAN_NOT_FIND_ARTIST.format(artist_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return iter(tracks).map(track_into_data).list()
