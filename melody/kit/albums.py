from uuid import UUID

from edgedb import NoDataError
from fastapi import status

from melody.kit.core import database, v1
from melody.kit.errors import Error, ErrorCode
from melody.kit.models import AlbumData

__all__ = ("get_album",)

CAN_NOT_FIND_ALBUM = "can not find the album with id `{}`"


@v1.get("/albums/{album_id}")
async def get_album(album_id: UUID) -> AlbumData:
    try:
        album = await database.query_album(album_id)

    except NoDataError:
        raise Error(
            CAN_NOT_FIND_ALBUM.format(album_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        ) from None

    else:
        return album.into_data()
