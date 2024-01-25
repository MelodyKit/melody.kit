from attrs import define, field
from yarl import URL

from melody.shared.constants import GET
from melody.shared.http import Route, SharedHTTPClient
from melody.shared.tokens import Tokens, authorization
from melody.spotify.models.track import TrackData

BASE_URL = URL("https://api.spotify.com/v1")


@define()
class HTTPClient(SharedHTTPClient):
    url: URL = field(default=BASE_URL, converter=URL)

    async def get_track(self, track_id: str, tokens: Tokens) -> TrackData:
        route = Route(GET, "/tracks/{track_id}").with_parameters(track_id=track_id)

        return await self.request_route(route, headers=authorization(tokens))  # type: ignore
