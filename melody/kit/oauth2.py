from secrets import token_urlsafe as token_url_safe
from typing import Optional
from uuid import UUID

from argon2.exceptions import VerifyMismatchError
from attrs import frozen
from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2AuthorizationCodeBearer

from melody.kit.core import config, database, hasher
from melody.kit.errors import AuthInvalid
from melody.kit.tokens import BoundToken, fetch_user_id_by_access_token
from melody.shared.constants import CODE_SIZE

INVALID_TOKEN = "invalid token"
INVALID_CLIENT_CREDENTIALS = "invalid client credentials"

TOKENS = "tokens"

AUTHORIZE = f"https://{config.open}.{config.domain}/authorize"

BASIC_DESCRIPTION = "This is used solely for sending `client_id` and `client_secret` to the server."

basic = HTTPBasic(description=BASIC_DESCRIPTION, auto_error=False)
scheme = OAuth2AuthorizationCodeBearer(AUTHORIZE, TOKENS, auto_error=False)


@frozen()
class ClientCredentials:
    client_id: UUID
    client_secret: str


async def bound_token_dependency(token: Optional[str] = Depends(scheme)) -> BoundToken:
    if token is None:
        raise AuthInvalid(INVALID_TOKEN)

    self_id = await fetch_user_id_by_access_token(token)

    if self_id is None:
        raise AuthInvalid(INVALID_TOKEN)

    return BoundToken(token, self_id)


async def token_dependency(token: Optional[str] = Depends(scheme)) -> UUID:
    bound_token = await bound_token_dependency(token)

    return bound_token.self_id


async def optional_token_dependency(token: Optional[str] = Depends(scheme)) -> Optional[UUID]:
    if token is None:
        return None

    return await token_dependency(token)


async def client_credentials_dependency(
    basic_credentials: Optional[HTTPBasicCredentials] = Depends(basic)
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


def authorization_code(size: int = CODE_SIZE) -> str:
    return token_url_safe(size)
