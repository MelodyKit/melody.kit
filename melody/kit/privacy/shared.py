from typing import Optional, Set
from uuid import UUID

from melody.kit.core import database
from melody.kit.scopes import USER_FOLLOWING_READ
from melody.kit.tokens.context import (
    ClientUserContext,
    Context,
    is_client_user_context,
    is_user_context,
)

__all__ = ("are_friends", "get_friends", "user_id_from_context")


async def are_friends(self_id: UUID, user_id: UUID) -> bool:
    return await database.check_user_friends(self_id=self_id, user_id=user_id)


async def get_friends(self_id: UUID) -> Optional[Set[UUID]]:
    return await database.query_user_friends_essential(user_id=self_id)


def client_user_has_access(context: ClientUserContext) -> bool:
    return context.scopes.has(USER_FOLLOWING_READ)


def user_id_from_context(context: Context) -> Optional[UUID]:
    return (
        context.user_id
        if is_user_context(context)
        or is_client_user_context(context)
        and client_user_has_access(context)
        else None
    )
