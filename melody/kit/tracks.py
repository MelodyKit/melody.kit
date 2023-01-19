from uuid import UUID

from edgedb import NoDataError
from fastapi import status

from melody.kit.core import database, v1
from melody.kit.errors import Error, ErrorCode
from melody.kit.models import TrackData

__all__ = ("get_track",)

CAN_NOT_FIND_TRACK = "can not find the track with id `{}`"


@v1.get("/tracks/{track_id}")
async def get_track(track_id: UUID) -> TrackData:
    try:
        track = await database.query_track(track_id)

    except NoDataError:
        raise Error(
            CAN_NOT_FIND_TRACK.format(track_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        ) from None

    else:
        return track.into_data()
