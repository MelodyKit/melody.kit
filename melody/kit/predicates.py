from typing import Optional
from uuid import UUID

from typing_aliases import AsyncPredicate

from melody.kit.core import database
from melody.kit.models.playlist import Playlist
from melody.kit.models.user import User


async def is_user_accessible_simple(user: User) -> bool:
    return user.privacy_type.is_public()


async def is_user_accessible(user: User, target_id: UUID) -> bool:
    user_id = user.id

    if user_id == target_id:
        return True

    user_privacy_type = user.privacy_type

    if user_privacy_type.is_private():
        return False

    if user_privacy_type.is_friends():
        return await database.check_user_friends(user_id=user_id, target_id=target_id)

    return True


def create_user_predicate(target_id: UUID) -> AsyncPredicate[User]:
    async def predicate(user: User) -> bool:
        return await is_user_accessible(user, target_id)

    return predicate


def user_predicate(user_id_option: Optional[UUID]) -> AsyncPredicate[User]:
    if user_id_option is None:
        return is_user_accessible_simple

    return create_user_predicate(user_id_option)


async def is_playlist_accessible_simple(playlist: Playlist) -> bool:
    return playlist.privacy_type.is_public() and playlist.user.privacy_type.is_public()


async def is_playlist_accessible(playlist: Playlist, user_id: UUID) -> bool:
    playlist_user = playlist.user
    playlist_user_id = playlist_user.id

    if user_id == playlist_user_id:
        return True

    playlist_privacy_type = playlist.privacy_type
    playlist_user_privacy_type = playlist_user.privacy_type

    private = playlist_privacy_type.is_private() or playlist_user_privacy_type.is_private()
    friends = playlist_privacy_type.is_friends() or playlist_user_privacy_type.is_friends()

    if private:
        return False

    if friends:
        return await database.check_user_friends(user_id=playlist_user_id, target_id=user_id)

    return True


def playlist_predicate(user_id_option: Optional[UUID]) -> AsyncPredicate[Playlist]:
    if user_id_option is None:
        return is_playlist_accessible_simple

    return create_playlist_predicate(user_id_option)


def create_playlist_predicate(user_id: UUID) -> AsyncPredicate[Playlist]:
    async def predicate(playlist: Playlist) -> bool:
        return await is_playlist_accessible(playlist, user_id)

    return predicate
