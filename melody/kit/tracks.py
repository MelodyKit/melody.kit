from uuid import UUID

from edgedb import NoDataError

from fastapi import status
from fastapi.exceptions import HTTPException

from melody.kit.core import database, v1
from melody.kit.models import TrackData

__all__ = ("get_track",)

CAN_NOT_FIND_TRACK = "can not find the track with id `{}`"


@v1.get("/tracks/{track_id}")
async def get_track(track_id: UUID) -> TrackData:
    try:
        track = await database.query_track(track_id)

    except NoDataError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=CAN_NOT_FIND_TRACK.format(track_id)
        )

    else:
        return track.into_data()
