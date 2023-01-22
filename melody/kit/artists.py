from uuid import UUID

from fastapi import status
from fastapi.responses import FileResponse

from melody.kit.core import database, v1
from melody.kit.enums import URIType
from melody.kit.errors import Error, ErrorCode
from melody.kit.models import ArtistData
from melody.kit.uri import URI

__all__ = ("get_artist", "get_artist_link")

CAN_NOT_FIND_ARTIST = "can not find the artist with id `{}`"


@v1.get("/artists/{artist_id}")
async def get_artist(artist_id: UUID) -> ArtistData:
    artist = await database.query_artist(artist_id)

    if artist is None:
        raise Error(
            CAN_NOT_FIND_ARTIST.format(artist_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return artist.into_data()


@v1.get("/artists/{artist_id}/link")
async def get_artist_link(artist_id: UUID) -> FileResponse:
    uri = URI(type=URIType.ARTIST, id=artist_id)

    path = await uri.create_link()

    return FileResponse(path)
