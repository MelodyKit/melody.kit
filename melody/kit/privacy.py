from typing import Optional, Set
from uuid import UUID

from melody.kit.core import database
from melody.kit.enums import PrivacyType
from melody.kit.models.playlist import PartialPlaylist
from melody.kit.models.user import User
from melody.shared.markers import unreachable

__all__ = (
    "friends_set",
    "are_friends",
    "process_privacy_type",
    "is_user_public",
    "is_user_accessible",
    "is_playlist_public",
    "is_playlist_accessible",
)


async def friends_set(user_id: UUID) -> Optional[Set[UUID]]:
    return await database.query_user_friend_ids(user_id=user_id)


async def are_friends(self_id: UUID, user_id: UUID) -> bool:
    return await database.check_user_friends(self_id=self_id, user_id=user_id)


def process_privacy_type(privacy_type: PrivacyType, friends: bool) -> bool:
    if privacy_type.is_private():
        return False

    if privacy_type.is_friends():
        return friends

    if privacy_type.is_public():
        return True

    unreachable()


def is_user_public(user: User) -> bool:
    return user.privacy_type.is_public()


def is_user_accessible(self_id: UUID, user: User, friends: bool) -> bool:
    user_id = user.id

    if self_id == user_id:
        return True

    return process_privacy_type(user.privacy_type, friends)


def is_playlist_public(playlist: PartialPlaylist) -> bool:
    return playlist.privacy_type.is_public()


def is_playlist_accessible(
    self_id: UUID, playlist: PartialPlaylist, user: User, friends: bool
) -> bool:
    user_id = user.id

    if self_id == user_id:
        return True

    return process_privacy_type(playlist.privacy_type, friends)
