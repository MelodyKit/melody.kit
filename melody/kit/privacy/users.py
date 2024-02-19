from typing import Optional
from uuid import UUID

from typing_aliases import Predicate

from melody.kit.core import database
from melody.kit.errors.users import UserInaccessible, UserNotFound
from melody.kit.models.user import User
from melody.kit.privacy.shared import are_friends, get_friends, user_id_from_context
from melody.kit.tokens.dependencies import TokenDependency

__all__ = (
    "check_user_accessible",
    "check_user_accessible_dependency",
    "create_user_accessible_predicate",
)


async def check_user_accessible(user_id: UUID, self_id: Optional[UUID] = None) -> None:
    user_privacy = await database.query_user_privacy(user_id=user_id)

    if user_privacy is None:
        raise UserNotFound(user_id)

    if self_id is None:
        if not user_privacy.is_accessible():
            raise UserInaccessible(user_id)

        return

    friends = await are_friends(self_id, user_id)

    if not user_privacy.is_accessible_by(self_id, friends):
        raise UserInaccessible(user_id)


async def check_user_accessible_dependency(user_id: UUID, context: TokenDependency) -> None:
    await check_user_accessible(user_id, user_id_from_context(context))


async def create_user_accessible_predicate(self_id: Optional[UUID] = None) -> Predicate[User]:
    if self_id is None:

        def predicate(user: User) -> bool:
            return user.privacy.is_accessible()

        return predicate

    friends = await get_friends(self_id)

    if friends is None:
        raise UserNotFound(self_id)

    def privacy_predicate(user: User) -> bool:
        return user.privacy.is_accessible_by(self_id, user.id in friends)

    return privacy_predicate
