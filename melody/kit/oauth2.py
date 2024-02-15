from typing import Generic, Optional, TypeVar
from typing_extensions import Annotated
from uuid import UUID

from argon2.exceptions import VerifyMismatchError
from attrs import frozen
from fastapi import Depends, Form, Security
from fastapi.requests import Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2, SecurityScopes

from melody.kit.contexts import (
    Context,
    UserBasedContext,
    UserContext,
    is_client_user_context,
    is_user_context,
)
from melody.kit.core import config, database, hasher
from melody.kit.errors import AuthExpected, AuthInvalid
from melody.kit.scopes import (
    SCOPE_SETUP,
    USER_FOLLOWING_READ,
    USER_FOLLOWING_WRITE,
    USER_IMAGE_READ,
    USER_IMAGE_WRITE,
    USER_LIBRARY_READ,
    USER_LIBRARY_WRITE,
    USER_PLAYLISTS_READ,
    USER_PLAYLISTS_WRITE,
    USER_SETTINGS_READ,
    USER_SETTINGS_WRITE,
    USER_STREAMS_READ,
    USER_STREAMS_WRITE,
    ScopeSetup,
)
from melody.kit.tokens import fetch_context_by_access_token, fetch_context_by_refresh_token
from melody.shared.tokens import AUTHORIZATION, AUTHORIZATION_SEPARATOR, Scopes
from melody.shared.typing import URLString

AUTHORIZE = f"https://{config.open}.{config.domain}/authorize"
TOKENS = "tokens"

AUTHORIZATION_CODE = "authorizationCode"
CLIENT_CREDENTIALS = "clientCredentials"
AUTHORIZATION_URL = "authorizationUrl"
TOKEN_URL = "tokenUrl"
SCOPES = "scopes"

EXPECTED_AUTH = "expected auth"
EXPECTED_TOKEN_TYPE = "expected `{}` token type"
expected_token_type = EXPECTED_TOKEN_TYPE.format


class OAuth2Scheme(OAuth2):
    def __init__(
        self,
        authorize_url: URLString,
        tokens_url: URLString,
        scope_setup: Optional[ScopeSetup] = None,
        description: Optional[str] = None,
    ) -> None:
        if scope_setup is None:
            scope_setup = {}

        flows = {
            AUTHORIZATION_CODE: {
                AUTHORIZATION_URL: str(authorize_url),
                TOKEN_URL: str(tokens_url),
                SCOPES: scope_setup,
            },
            CLIENT_CREDENTIALS: {TOKEN_URL: str(tokens_url)},
        }

        super().__init__(flows=flows, description=description)  # type: ignore[arg-type]

    async def __call__(self, request: Request) -> str:
        authorization = request.headers.get(AUTHORIZATION)

        if authorization is None:
            raise AuthExpected(EXPECTED_AUTH)

        token_type, _, token = authorization.partition(AUTHORIZATION_SEPARATOR)

        expected_type = config.token.type

        if token_type != expected_type:
            raise AuthInvalid(expected_token_type(expected_type))

        return token


scheme = OAuth2Scheme(authorize_url=AUTHORIZE, tokens_url=TOKENS, scope_setup=SCOPE_SETUP)

BASIC_DESCRIPTION = "This is used solely for sending `client_id` and `client_secret` credentials."

basic = HTTPBasic(description=BASIC_DESCRIPTION, auto_error=False)


@frozen()
class ClientCredentials:
    id: UUID
    secret: str


INVALID_CLIENT_CREDENTIALS = "invalid client credentials"

BasicCredentialsDependency = Annotated[Optional[HTTPBasicCredentials], Depends(basic)]


async def client_credentials_dependency(
    basic_credentials: BasicCredentialsDependency,
) -> ClientCredentials:
    if basic_credentials is None:
        raise AuthInvalid(INVALID_CLIENT_CREDENTIALS)

    client_id_string = basic_credentials.username

    try:
        client_id = UUID(client_id_string)

    except ValueError:
        raise AuthInvalid(INVALID_CLIENT_CREDENTIALS) from None

    client_secret = basic_credentials.password

    client = await database.query_client(client_id=client_id)

    if client is None:
        raise AuthInvalid(INVALID_CLIENT_CREDENTIALS)

    secret_hash = client.secret_hash

    try:
        hasher.verify(secret_hash, client_secret)

    except VerifyMismatchError:
        raise AuthInvalid(INVALID_CLIENT_CREDENTIALS) from None

    if hasher.check_needs_rehash(secret_hash):
        secret_hash = hasher.hash(client_secret)

        await database.update_client_secret_hash(client_id=client_id, secret_hash=secret_hash)

    return ClientCredentials(client_id, client_secret)


ClientCredentialsDependency = Annotated[ClientCredentials, Depends(client_credentials_dependency)]


async def optional_client_credentials_dependency(
    basic_credentials: BasicCredentialsDependency,
) -> Optional[ClientCredentials]:
    return (
        None
        if basic_credentials is None
        else await client_credentials_dependency(basic_credentials)
    )


OptionalClientCredentialsDependency = Annotated[
    Optional[ClientCredentials], Depends(optional_client_credentials_dependency)
]


SchemeTokenDependency = Annotated[str, Depends(scheme)]


C = TypeVar("C", bound=Context)


@frozen()
class BoundToken(Generic[C]):
    token: str
    context: C


INVALID_TOKEN = "invalid token"
EXPECTED_USER_TOKEN = "expected user token"


async def bound_user_token_dependency(token: SchemeTokenDependency) -> BoundToken[UserContext]:
    context = await fetch_context_by_access_token(token)

    if context is None:
        raise AuthInvalid(INVALID_TOKEN)

    if is_user_context(context):
        return BoundToken(token, context)

    raise AuthInvalid(EXPECTED_USER_TOKEN)


BoundUserTokenDependency = Annotated[BoundToken[UserContext], Depends(bound_user_token_dependency)]


async def user_token_dependency(bound_user_token: BoundUserTokenDependency) -> UserContext:
    return bound_user_token.context


UserTokenDependency = Annotated[UserContext, Depends(user_token_dependency)]


EXPECTED_USER_BASED_TOKEN = "expected user-based token"

MISSING_SCOPE = "missing scope: `{}`"
missing_scope = MISSING_SCOPE.format


async def bound_user_based_token_dependency(
    security_scopes: SecurityScopes, token: SchemeTokenDependency
) -> BoundToken[UserBasedContext]:
    context = await fetch_context_by_access_token(token)

    if context is None:
        raise AuthInvalid(INVALID_TOKEN)

    if is_user_context(context):
        return BoundToken(token, context)

    scopes = frozenset(security_scopes.scopes)

    if is_client_user_context(context):
        missing = scopes.difference(context.scopes.tokens)

        if missing:
            scope = Scopes(missing).scope

            raise AuthInvalid(missing_scope(scope))

        return BoundToken(token, context)

    raise AuthInvalid(EXPECTED_USER_BASED_TOKEN)


BoundUserBasedTokenDependency = Annotated[
    BoundToken[UserBasedContext], Depends(bound_user_based_token_dependency)
]


async def user_based_token_dependency(
    bound_user_based_token: BoundUserBasedTokenDependency,
) -> UserBasedContext:
    return bound_user_based_token.context


UserBasedTokenDependency = Annotated[UserBasedContext, Depends(user_based_token_dependency)]


async def bound_token_dependency(token: SchemeTokenDependency) -> BoundToken[Context]:
    context = await fetch_context_by_access_token(token)

    if context is None:
        raise AuthInvalid(INVALID_TOKEN)

    return BoundToken(token, context)


BoundTokenDependency = Annotated[BoundToken[Context], Depends(bound_token_dependency)]


async def token_dependency(bound_token: BoundTokenDependency) -> Context:
    return bound_token.context


TokenDependency = Annotated[Context, Depends(token_dependency)]


FollowingReadTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_FOLLOWING_READ])
]
FollowingWriteTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_FOLLOWING_WRITE])
]
LibraryReadTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_LIBRARY_READ])
]
LibraryWriteTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_LIBRARY_WRITE])
]
PlaylistsReadTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_PLAYLISTS_READ])
]
PlaylistsWriteTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_PLAYLISTS_WRITE])
]
SettingsReadTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_SETTINGS_READ])
]
SettingsWriteTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_SETTINGS_WRITE])
]
ImageReadTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_IMAGE_READ])
]
ImageWriteTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_IMAGE_WRITE])
]
StreamsReadTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_STREAMS_READ])
]
StreamsWriteTokenDependency = Annotated[
    UserBasedContext, Security(user_based_token_dependency, scopes=[USER_STREAMS_WRITE])
]


INVALID_REFRESH_TOKEN = "invalid refresh token"

FormRefreshTokenDependency = Annotated[str, Form()]
OptionalFormRefreshTokenDependency = Annotated[Optional[str], Form()]


async def refresh_token_dependency(refresh_token: FormRefreshTokenDependency) -> Context:
    context = await fetch_context_by_refresh_token(refresh_token)

    if context is None:
        raise AuthInvalid(INVALID_REFRESH_TOKEN)

    return context


RefreshTokenDependency = Annotated[Context, Depends(refresh_token_dependency)]


async def optional_refresh_token_dependency(
    refresh_token: OptionalFormRefreshTokenDependency = None,
) -> Optional[Context]:
    return None if refresh_token is None else await refresh_token_dependency(refresh_token)


OptionalRefreshTokenDependency = Annotated[
    Optional[Context], Depends(optional_refresh_token_dependency)
]
