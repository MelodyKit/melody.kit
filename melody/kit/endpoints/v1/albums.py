from uuid import UUID

from fastapi.responses import FileResponse
from iters import iter

from melody.kit.core import database, v1
from melody.kit.enums import EntityType
from melody.kit.errors import NotFound
from melody.kit.link import generate_code_for_uri
from melody.kit.models.album import AlbumData, AlbumTracksData, album_into_data
from melody.kit.models.track import partial_track_into_data
from melody.kit.tags import ALBUMS, LINKS, TRACKS
from melody.kit.uri import URI

__all__ = ("get_album", "get_album_link", "get_album_tracks")

CAN_NOT_FIND_ALBUM = "can not find the album with ID `{}`"


@v1.get(
    "/albums/{album_id}",
    tags=[ALBUMS],
    summary="Fetches the album with the given ID.",
)
async def get_album(album_id: UUID) -> AlbumData:
    album = await database.query_album(album_id)

    if album is None:
        raise NotFound(CAN_NOT_FIND_ALBUM.format(album_id))

    return album_into_data(album)


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
async def get_album_tracks(album_id: UUID) -> AlbumTracksData:
    tracks = await database.query_album_tracks(album_id)

    if tracks is None:
        raise NotFound(CAN_NOT_FIND_ALBUM.format(album_id))

    return iter(tracks).map(partial_track_into_data).list()