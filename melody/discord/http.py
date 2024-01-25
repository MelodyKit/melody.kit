from attrs import define, field
from yarl import URL

from melody.discord.models.entity import EntityData
from melody.shared.constants import GET
from melody.shared.http import Route, SharedHTTPClient
from melody.shared.tokens import Tokens
from melody.shared.typing import Data

BASE_URL = URL("https://discord.com/api/v10")


class AuthorizationData(Data):
    Authorization: str


AUTHORIZATION_HEADER = "{type} {content}"
authorization_header = AUTHORIZATION_HEADER.format


def authorization(tokens: Tokens) -> AuthorizationData:
    return AuthorizationData(
        Authorization=authorization_header(type=tokens.type, content=tokens.token)
    )


@define()
class HTTPClient(SharedHTTPClient):
    url: URL = field(default=BASE_URL, converter=URL)

    async def get_self(self, tokens: Tokens) -> EntityData:
        route = Route(GET, "/users/@me")

        headers = authorization(tokens)

        return await self.request_route(route, headers=headers)  # type: ignore[return-value]
