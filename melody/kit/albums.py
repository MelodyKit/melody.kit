from uuid import UUID

from fastapi import status
from fastapi.responses import FileResponse
from iters import iter

from melody.kit.core import database, v1
from melody.kit.enums import URIType
from melody.kit.errors import Error, ErrorCode
from melody.kit.models import AlbumData, AlbumTracksData, track_into_data
from melody.kit.uri import URI

__all__ = ("get_album", "get_album_link", "get_album_tracks")

CAN_NOT_FIND_ALBUM = "can not find the album with id `{}`"


@v1.get("/albums/{album_id}")
async def get_album(album_id: UUID) -> AlbumData:
    album = await database.query_album(album_id)

    if album is None:
        raise Error(
            CAN_NOT_FIND_ALBUM.format(album_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return album.into_data()


@v1.get("/albums/{album_id}/link")
async def get_album_link(album_id: UUID) -> FileResponse:
    uri = URI(type=URIType.ALBUM, id=album_id)

    path = await uri.create_link()

    return FileResponse(path)


@v1.get("/albums/{album_id}/tracks")
async def get_album_tracks(album_id: UUID) -> AlbumTracksData:
    tracks = await database.query_album_tracks(album_id)

    if tracks is None:
        raise Error(
            CAN_NOT_FIND_ALBUM.format(album_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return iter(tracks).map(track_into_data).list()
