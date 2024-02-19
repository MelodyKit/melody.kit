from typing import Optional
from uuid import UUID

from argon2.exceptions import VerifyMismatchError
from fastapi import Depends, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing_extensions import Annotated

from melody.kit.clients.credentials import ClientCredentials
from melody.kit.core import database, hasher
from melody.kit.errors.auth import (
    AuthClientCredentialsExpected,
    AuthClientCredentialsInvalid,
    AuthClientCredentialsNotFound,
    AuthClientCredentialsSecretMismatch,
)

__all__ = (
    # dependencies
    "FormClientCredentialsDependency",
    "ClientCredentialsDependency",
    "OptionalClientCredentialsDependency",
    # dependables
    "form_client_credentials_dependency",
    "client_credentials_dependency",
    "optional_client_credentials_dependency",
)

BASIC_DESCRIPTION = "This is used solely for sending `client_id` and `client_secret` credentials."

basic = HTTPBasic(description=BASIC_DESCRIPTION, auto_error=False)

BasicCredentialsDependency = Annotated[Optional[HTTPBasicCredentials], Depends(basic)]


ClientIDDependency = Annotated[UUID, Form()]
ClientSecretDependency = Annotated[str, Form()]


async def form_client_credentials_dependency(
    client_id: ClientIDDependency, client_secret: ClientSecretDependency
) -> ClientCredentials:
    client_info = await database.query_client_info(client_id=client_id)

    if client_info is None:
        raise AuthClientCredentialsNotFound()

    secret_hash = client_info.secret_hash

    try:
        hasher.verify(client_secret, secret_hash)

    except VerifyMismatchError:
        raise AuthClientCredentialsSecretMismatch() from None

    return ClientCredentials(client_id, client_secret)


FormClientCredentialsDependency = Annotated[
    ClientCredentials, Depends(form_client_credentials_dependency)
]


async def client_credentials_dependency(
    basic_credentials: BasicCredentialsDependency,
) -> ClientCredentials:
    if basic_credentials is None:
        raise AuthClientCredentialsExpected()

    client_id_string = basic_credentials.username

    try:
        client_id = UUID(client_id_string)

    except ValueError:
        raise AuthClientCredentialsInvalid()

    client_secret = basic_credentials.password

    return await form_client_credentials_dependency(client_id, client_secret)


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
