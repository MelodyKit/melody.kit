from attrs import define, field
from httpx import AsyncClient

from melody.shared.constants import GET
from melody.shared.http import HTTPClient as SharedHTTPClient
from melody.shared.http import Route
from melody.spotify.models.track import TrackData

BASE_URL = "https://api.spotify.com/v1"


def async_client_factory(base_url: str = BASE_URL) -> AsyncClient:
    return AsyncClient(base_url=base_url)


@define()
class HTTPClient(SharedHTTPClient):
    client: AsyncClient = field(factory=async_client_factory)

    async def get_track(self, track_id: str) -> TrackData:
        route = Route(GET, "/tracks/{track_id}", track_id=track_id)  # type: ignore

        return await self.request_route(route)  # type: ignore
