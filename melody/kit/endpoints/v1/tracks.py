from uuid import UUID

from fastapi.responses import FileResponse

from melody.kit.code import generate_code_for_uri
from melody.kit.core import database, v1
from melody.kit.enums import EntityType, Tag
from melody.kit.errors import NotFound
from melody.kit.models.tracks import TrackData
from melody.kit.uri import URI

__all__ = ("get_track", "get_track_link")

CAN_NOT_FIND_TRACK = "can not find the track with ID `{}`"
can_not_find_track = CAN_NOT_FIND_TRACK.format


@v1.get(
    "/tracks/{track_id}",
    tags=[Tag.TRACKS],
    summary="Fetches the track.",
)
async def get_track(track_id: UUID) -> TrackData:
    track = await database.query_track(track_id=track_id)

    if track is None:
        raise NotFound(can_not_find_track(track_id))

    return track.into_data()


@v1.get(
    "/tracks/{track_id}/link",
    tags=[Tag.TRACKS],
    summary="Fetches the track's link.",
)
async def get_track_link(track_id: UUID) -> FileResponse:
    uri = URI(type=EntityType.TRACK, id=track_id)

    path = await generate_code_for_uri(uri)

    return FileResponse(path)
