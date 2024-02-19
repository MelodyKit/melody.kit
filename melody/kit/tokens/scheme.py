from typing import Any, Optional

from fastapi.requests import Request
from fastapi.security import OAuth2
from typing_aliases import StringDict
from yarl import URL

from melody.kit.core import config
from melody.kit.errors.auth import (
    AuthAccessTokenExpected,
    AuthAccessTokenExpectedType,
    AuthAccessTokenInvalid,
)
from melody.kit.scopes import DESCRIBED_SCOPES, DescribedScopes
from melody.shared.converter import unstructure_url
from melody.shared.tokens import AUTHORIZATION, AUTHORIZATION_SEPARATOR
from melody.shared.typing import URLString

__all__ = ("OAuth2Scheme", "oauth2_scheme")

AUTHORIZATION_CODE = "authorizationCode"
CLIENT_CREDENTIALS = "clientCredentials"
AUTHORIZATION_URL = "authorizationUrl"
TOKEN_URL = "tokenUrl"
SCOPES = "scopes"


def restructure_url(url: URLString) -> str:
    return unstructure_url(URL(url))


class OAuth2Scheme(OAuth2):
    def __init__(
        self,
        authorize_url: URLString,
        tokens_url: URLString,
        scopes: Optional[DescribedScopes] = None,
        description: Optional[str] = None,
    ) -> None:
        if scopes is None:
            scopes = {}

        flows: StringDict[StringDict[Any]] = {
            AUTHORIZATION_CODE: {
                AUTHORIZATION_URL: restructure_url(authorize_url),
                TOKEN_URL: restructure_url(tokens_url),
                SCOPES: scopes,
            },
            CLIENT_CREDENTIALS: {TOKEN_URL: restructure_url(tokens_url)},
        }

        super().__init__(flows=flows, description=description)

    async def __call__(self, request: Request) -> str:
        authorization = request.headers.get(AUTHORIZATION)

        if authorization is None:
            raise AuthAccessTokenExpected()

        token_type, _, token = authorization.partition(AUTHORIZATION_SEPARATOR)

        if not token:
            raise AuthAccessTokenInvalid()

        expected_type = config.token.type

        if token_type != expected_type:
            raise AuthAccessTokenExpectedType(expected_type)

        return token


AUTHORIZE_URL = f"https://{config.open}.{config.domain}/authorize"
TOKENS_URL = "tokens"

oauth2_scheme = OAuth2Scheme(
    authorize_url=AUTHORIZE_URL, tokens_url=TOKENS_URL, scopes=DESCRIBED_SCOPES
)
