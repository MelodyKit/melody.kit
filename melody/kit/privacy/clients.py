from uuid import UUID

from melody.kit.core import database
from melody.kit.errors.clients import ClientInaccessible, ClientNotFound
from melody.kit.tokens.dependencies import UserTokenDependency

__all__ = ("check_client_changeable", "check_client_changeable_dependency")


async def check_client_changeable(client_id: UUID, user_id: UUID) -> None:
    client = await database.query_client_info(client_id=client_id)

    if client is None:
        raise ClientNotFound(client_id)

    if client.creator_id != user_id:
        raise ClientInaccessible(client_id)


async def check_client_changeable_dependency(client_id: UUID, context: UserTokenDependency) -> None:
    await check_client_changeable(client_id, context.user_id)
