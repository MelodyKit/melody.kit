from uuid import UUID

from fastapi import Depends

from melody.kit.core import database, v1
from melody.kit.enums import Tag
from melody.kit.errors import NotFound
from melody.kit.models.client import ClientData
from melody.kit.oauth2 import token_dependency

__all__ = ("get_client",)

CAN_NOT_FIND_CLIENT = "can not find the client with ID `{}`"
can_not_find_client = CAN_NOT_FIND_CLIENT.format


@v1.get(
    "/clients/{client_id}",
    tags=[Tag.CLIENTS],
    summary="Fetches the client.",
    dependencies=[Depends(token_dependency)],
)
async def get_client(client_id: UUID) -> ClientData:
    client = await database.query_client(client_id=client_id)

    if client is None:
        raise NotFound(can_not_find_client(client_id))

    return client.into_data()
