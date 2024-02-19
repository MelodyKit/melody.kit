from typing import Optional
from uuid import UUID

from fastapi import Body, Depends
from typing_extensions import Annotated

from melody.kit.clients.credentials import ClientCredentials, ClientCredentialsData
from melody.kit.core import database, hasher, v1
from melody.kit.enums import Tag
from melody.kit.errors.clients import ClientNotFound
from melody.kit.models.client import ClientData
from melody.kit.privacy.clients import check_client_changeable_dependency
from melody.kit.secrets import generate_secret
from melody.kit.tokens.dependencies import UserTokenDependency, token_dependency

__all__ = ("get_client",)

NameDependency = Annotated[str, Body()]
OptionalDescriptionDependency = Annotated[Optional[str], Body()]


class CreateClientPayload:
    def __init__(
        self,
        name: NameDependency,
        description: OptionalDescriptionDependency = None,
    ) -> None:
        self.name = name
        self.desciption = description


CreateClientPayloadDependency = Annotated[CreateClientPayload, Depends()]


@v1.post(
    "/clients",
    tags=[Tag.CLIENTS],
    summary="Creates a new client.",
)
async def create_client(
    context: UserTokenDependency,
    payload: CreateClientPayloadDependency,
) -> ClientCredentialsData:
    secret = generate_secret()

    secret_hash = hasher.hash(secret)

    base = await database.insert_client(
        name=payload.name,
        description=payload.desciption,
        secret_hash=secret_hash,
        creator_id=context.user_id,
    )

    client_credentials = ClientCredentials(base.id, secret)

    return client_credentials.into_data()


@v1.get(
    "/clients/{client_id}",
    tags=[Tag.CLIENTS],
    summary="Fetches the client.",
    dependencies=[Depends(token_dependency)],
)
async def get_client(client_id: UUID) -> ClientData:
    client = await database.query_client(client_id=client_id)

    if client is None:
        raise ClientNotFound(client_id)

    return client.into_data()


@v1.delete(
    "/clients/{client_id}",
    tags=[Tag.CLIENTS],
    summary="Deletes the client.",
    dependencies=[Depends(check_client_changeable_dependency)],
)
async def delete_client(client_id: UUID) -> None:
    await database.delete_client(client_id=client_id)


OptionalNameDependency = Annotated[Optional[str], Body()]


class UpdateClientPayload:
    def __init__(
        self,
        name: OptionalNameDependency = None,
        description: OptionalDescriptionDependency = None,
    ) -> None:
        self.name = name
        self.description = description


UpdateClientPayloadDependency = Annotated[UpdateClientPayload, Depends()]


@v1.put(
    "/clients/{client_id}",
    tags=[Tag.CLIENTS],
    summary="Updates the client.",
    dependencies=[Depends(check_client_changeable_dependency)],
)
async def update_client(
    client_id: UUID,
    payload: UpdateClientPayloadDependency,
) -> None:
    name = payload.name
    description = payload.description

    if name is None and description is None:
        return  # nothing to update

    client = await database.query_client(client_id=client_id)

    if client is None:
        raise ClientNotFound(client_id)

    if name is None:
        name = client.name

    if description is None:
        description = client.description

    await database.update_client(client_id=client_id, name=name, description=description)
