from aiohttp import BasicAuth
from attrs import define, field
from yarl import URL

from melody.discord.models.entity import EntityData
from melody.discord.models.tokens import Tokens, TokensData
from melody.kit.connections import callback_url
from melody.kit.enums import Connection
from melody.shared.constants import AUTHORIZATION_CODE, GET, POST
from melody.shared.http import Route, SharedHTTPClient
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

    async def get_tokens(self, code: str, client_id: str, client_secret: str) -> TokensData:
        route = Route(POST, "/oauth2/token")

        data = dict(
            grant_type=AUTHORIZATION_CODE,
            code=code,
            redirect_uri=str(callback_url(Connection.DISCORD)),
        )

        auth = BasicAuth(client_id, client_secret)

        return await self.request_route(route, data=data, auth=auth)  # type: ignore[return-value]
