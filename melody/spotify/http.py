from attrs import define, field
from yarl import URL

from melody.shared.constants import CLIENT_CREDENTIALS, GET, POST
from melody.shared.http import Route, SharedHTTPClient
from melody.shared.typing import Data
from melody.spotify.models.tokens import Tokens, TokensData
from melody.spotify.models.track import TrackData

BASE_URL = URL("https://api.spotify.com/v1")
OAUTH_TOKEN_URL = URL("https://accounts.spotify.com/api/token")
OAUTH_AUTHORIZE_URL = URL("https://accounts.spotify.com/authorize")


class AuthorizationData(Data):
    Authorization: str


AUTHORIZATION_HEADER = "{} {}"
authorization_header = AUTHORIZATION_HEADER.format


def authorization(tokens: Tokens) -> AuthorizationData:
    return AuthorizationData(Authorization=authorization_header(tokens.type, tokens.token))


@define()
class HTTPClient(SharedHTTPClient):
    url: URL = field(default=BASE_URL, converter=URL)
    oauth_token_url: URL = field(default=OAUTH_TOKEN_URL, converter=URL)
    oauth_authorize_url: URL = field(default=OAUTH_AUTHORIZE_URL, converter=URL)

    async def get_track(self, track_id: str, tokens: Tokens) -> TrackData:
        route = Route(GET, "/tracks/{track_id}").with_parameters(track_id=track_id)

        return await self.request_route(route, headers=authorization(tokens))  # type: ignore

    async def get_client_credentials(self, client_id: str, client_secret: str) -> TokensData:
        data = dict(
            grant_type=CLIENT_CREDENTIALS,
            client_id=client_id,
            client_secret=client_secret,
        )

        return await self.request(POST, self.oauth_token_url, data=data)  # type: ignore
