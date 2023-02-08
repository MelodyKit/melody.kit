from attrs import define, field

from melody.spotify.http import HTTPClient
from melody.spotify.models.track import Track

__all__ = ("Client",)


@define()
class Client:
    http: HTTPClient = field(factory=HTTPClient)

    async def get_track(self, track_id: str) -> Track:
        data = await self.http.get_track(track_id)

        return Track.from_data(data).attach_client(self)
