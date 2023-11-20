from typing import TypedDict as Data

from attrs import define, field
from httpx import AsyncClient

from melody.shared.constants import CLIENT_CREDENTIALS, GET, POST
from melody.shared.http import HTTPClient as SharedHTTPClient
from melody.shared.http import Route
from melody.spotify.models.tokens import Tokens, TokensData
from melody.spotify.models.track import TrackData

BASE_URL = "https://api.spotify.com/v1"
OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"
OAUTH_AUTHORIZE_URL = "https://accounts.spotify.com/authorize"


def async_client_factory(base_url: str = BASE_URL) -> AsyncClient:
    return AsyncClient(base_url=base_url)


class AuthorizationData(Data):
    Authorization: str


AUTHORIZATION_HEADER = "{} {}"
authorization_header = AUTHORIZATION_HEADER.format


def authorization(tokens: Tokens) -> AuthorizationData:
    return AuthorizationData(Authorization=authorization_header(tokens.type, tokens.token))


@define()
class HTTPClient(SharedHTTPClient):
    client: AsyncClient = field(factory=async_client_factory)

    oauth_token_url: str = field(default=OAUTH_TOKEN_URL)
    oauth_authorize_url: str = field(default=OAUTH_AUTHORIZE_URL)

    async def get_track(self, track_id: str, tokens: Tokens) -> TrackData:
        route = Route(GET, "/tracks/{track_id}", track_id=track_id)  # type: ignore

        return await self.request_route(route, headers=authorization(tokens))  # type: ignore

    async def get_client_credentials(self, client_id: str, client_secret: str) -> TokensData:
        route = Route(POST, self.oauth_token_url)

        data = dict(grant_type=CLIENT_CREDENTIALS, client_id=client_id, client_secret=client_secret)

        return await self.request_route(route, data=data)  # type: ignore
