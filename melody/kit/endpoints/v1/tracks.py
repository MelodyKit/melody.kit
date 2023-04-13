from uuid import UUID

from fastapi.responses import FileResponse

from melody.kit.core import database, v1
from melody.kit.enums import EntityType
from melody.kit.errors import NotFound
from melody.kit.link import generate_code_for_uri
from melody.kit.models.track import TrackData, track_into_data
from melody.kit.tags import LINKS, TRACKS
from melody.kit.uri import URI

__all__ = ("get_track", "get_track_link")

CAN_NOT_FIND_TRACK = "can not find the track with ID `{}`"


@v1.get(
    "/tracks/{track_id}",
    tags=[TRACKS],
    summary="Fetches the track with the given ID.",
)
async def get_track(track_id: UUID) -> TrackData:
    track = await database.query_track(track_id)

    if track is None:
        raise NotFound(CAN_NOT_FIND_TRACK.format(track_id))

    return track_into_data(track)


@v1.get(
    "/tracks/{track_id}/link",
    tags=[TRACKS, LINKS],
    summary="Fetches the track link with the given ID.",
)
async def get_track_link(track_id: UUID) -> FileResponse:
    uri = URI(type=EntityType.TRACK, id=track_id)

    path = await generate_code_for_uri(uri)

    return FileResponse(path)
