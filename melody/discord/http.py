from attrs import define, field
from yarl import URL

from melody.discord.models.entity import EntityData
from melody.shared.constants import GET
from melody.shared.http import Route, SharedHTTPClient
from melody.shared.tokens import Tokens, authorization

BASE_URL = URL("https://discord.com/api/v10")


@define()
class HTTPClient(SharedHTTPClient):
    url: URL = field(default=BASE_URL, converter=URL)

    async def get_self(self, tokens: Tokens) -> EntityData:
        route = Route(GET, "/users/@me")

        headers = authorization(tokens)

        return await self.request_route(route, headers=headers)  # type: ignore[return-value]
