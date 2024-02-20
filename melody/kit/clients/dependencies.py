from typing import Optional
from uuid import UUID

from argon2.exceptions import VerifyMismatchError
from fastapi import Depends, Form
from typing_extensions import Annotated

from melody.kit.clients.credentials import ClientCredentials
from melody.kit.core import database, hasher
from melody.kit.errors.auth import (
    AuthClientCredentialsNotFound,
    AuthClientCredentialsSecretMismatch,
)

__all__ = (
    # dependencies
    "ClientCredentialsDependency",
    "OptionalClientCredentialsDependency",
    # dependables
    "client_credentials_dependency",
    "optional_client_credentials_dependency",
)

ClientIDDependency = Annotated[UUID, Form()]
ClientSecretDependency = Annotated[str, Form()]


async def client_credentials_dependency(
    client_id: ClientIDDependency, client_secret: ClientSecretDependency
) -> ClientCredentials:
    client_info = await database.query_client_info(client_id=client_id)

    if client_info is None:
        raise AuthClientCredentialsNotFound()

    secret_hash = client_info.secret_hash

    try:
        hasher.verify(secret_hash, client_secret)

    except VerifyMismatchError:
        raise AuthClientCredentialsSecretMismatch() from None

    return ClientCredentials(client_id, client_secret)


ClientCredentialsDependency = Annotated[ClientCredentials, Depends(client_credentials_dependency)]

OptionalClientIDDependency = Annotated[Optional[UUID], Form()]
OptionalClientSecretDependency = Annotated[Optional[str], Form()]


async def optional_client_credentials_dependency(
    client_id: OptionalClientIDDependency = None,
    client_secret: OptionalClientSecretDependency = None,
) -> Optional[ClientCredentials]:
    return (
        None
        if client_id is None or client_secret is None
        else await client_credentials_dependency(client_id, client_secret)
    )


OptionalClientCredentialsDependency = Annotated[
    Optional[ClientCredentials], Depends(optional_client_credentials_dependency)
]
