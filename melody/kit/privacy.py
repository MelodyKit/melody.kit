from typing import Optional, Set
from uuid import UUID

from typing_aliases import Predicate

from melody.kit.contexts import Context, is_client_user_context, is_user_context
from melody.kit.core import database
from melody.kit.errors import Forbidden, NotFound
from melody.kit.models.playlist import Playlist
from melody.kit.models.user import User
from melody.kit.oauth2 import PlaylistsWriteTokenDependency, TokenDependency
from melody.kit.scopes import USER_FOLLOWING_READ
from melody.kit.totp import TwoFactorTokenDependency


async def are_friends(self_id: UUID, user_id: UUID) -> bool:
    return await database.check_user_friends(self_id=self_id, user_id=user_id)


async def get_friends(self_id: UUID) -> Optional[Set[UUID]]:
    return await database.query_user_friends_essential(user_id=self_id)


CAN_NOT_FIND_USER = "can not find the user with ID `{}`"
can_not_find_user = CAN_NOT_FIND_USER.format

INACCESSIBLE_USER = "the user with ID `{}` is inaccessible"
inaccessible_user = INACCESSIBLE_USER.format


def self_id_from_context(context: Context) -> Optional[UUID]:
    return (
        context.user_id
        if is_user_context(context)
        or (is_client_user_context(context) and context.scopes.has(USER_FOLLOWING_READ))
        else None
    )


async def check_user_accessible(user_id: UUID, self_id: Optional[UUID] = None) -> None:
    user_privacy = await database.query_user_privacy(user_id=user_id)

    if user_privacy is None:
        raise NotFound(can_not_find_user(user_id))

    if self_id is None:
        if not user_privacy.is_accessible():
            raise Forbidden(inaccessible_user(user_id))

        return

    friends = await are_friends(self_id, user_id)

    if not user_privacy.is_accessible_by(self_id, friends):
        raise Forbidden(inaccessible_user(user_id))


async def check_user_accessible_dependency(user_id: UUID, context: TokenDependency) -> None:
    await check_user_accessible(user_id, self_id_from_context(context))


async def create_user_accessible_predicate(self_id: Optional[UUID] = None) -> Predicate[User]:
    if self_id is None:

        def predicate(user: User) -> bool:
            return user.privacy.is_accessible()

        return predicate

    friends = await get_friends(self_id)

    if friends is None:
        raise NotFound(can_not_find_user(self_id))

    def privacy_predicate(user: User) -> bool:
        return user.privacy.is_accessible_by(self_id, user.id in friends)

    return privacy_predicate


CAN_NOT_FIND_PLAYLIST = "can not find the playlist with ID `{}`"
can_not_find_playlist = CAN_NOT_FIND_PLAYLIST.format

INACCESSIBLE_PLAYLIST = "the playlist with ID `{}` is inaccessible"
inaccessible_playlist = INACCESSIBLE_PLAYLIST.format


async def check_playlist_accessible(playlist_id: UUID, self_id: Optional[UUID] = None) -> None:
    playlist_privacy = await database.query_playlist_privacy(playlist_id=playlist_id)

    if playlist_privacy is None:
        raise NotFound(can_not_find_playlist(playlist_id))

    if self_id is None:
        if not playlist_privacy.is_accessible():
            raise Forbidden(inaccessible_playlist(playlist_id))

        return

    friends = await are_friends(self_id, playlist_privacy.owner.id)

    if not playlist_privacy.is_accessible_by(self_id, friends):
        raise Forbidden(inaccessible_playlist(playlist_id))


async def check_playlist_accessible_dependency(playlist_id: UUID, context: TokenDependency) -> None:
    await check_playlist_accessible(playlist_id, self_id_from_context(context))


async def check_playlist_changeable(playlist_id: UUID, self_id: Optional[UUID] = None) -> None:
    playlist_privacy = await database.query_playlist_privacy(playlist_id=playlist_id)

    if playlist_privacy is None:
        raise NotFound(can_not_find_playlist(playlist_id))

    if self_id is None or playlist_privacy.owner.id != self_id:
        raise Forbidden(inaccessible_playlist(playlist_id))


async def check_playlist_changeable_dependency(
    playlist_id: UUID, context: PlaylistsWriteTokenDependency
) -> None:
    await check_playlist_changeable(playlist_id, self_id_from_context(context))


async def create_partial_playlist_accessible_predicate(
    owner_id: UUID, self_id: Optional[UUID] = None
) -> Predicate[Playlist]:
    owner = await database.query_user_privacy(owner_id)

    if owner is None:
        raise NotFound(can_not_find_user(owner_id))

    if self_id is None:

        def predicate(playlist: Playlist) -> bool:
            return playlist.privacy_with(owner).is_accessible()

        return predicate

    friends = await get_friends(self_id)

    if friends is None:
        raise NotFound(can_not_find_user(self_id))

    def privacy_predicate(playlist: Playlist) -> bool:
        return playlist.privacy_with(owner).is_accessible_by(self_id, owner_id in friends)

    return privacy_predicate


async def create_playlist_accessible_predicate(
    self_id: Optional[UUID] = None,
) -> Predicate[Playlist]:
    if self_id is None:

        def predicate(playlist: Playlist) -> bool:
            return playlist.privacy.is_accessible()

        return predicate

    friends = await get_friends(self_id)

    if friends is None:
        raise NotFound(can_not_find_user(self_id))

    def privacy_predicate(playlist: Playlist) -> bool:
        playlist_privacy = playlist.privacy

        return playlist_privacy.is_accessible_by(self_id, playlist_privacy.owner.id in friends)

    return privacy_predicate


CAN_NOT_FIND_CLIENT = "can not find the client with ID `{}`"
can_not_find_client = CAN_NOT_FIND_CLIENT.format

INACCESSIBLE_CLIENT = "the client with ID `{}` is inaccessible"
inaccessible_client = INACCESSIBLE_CLIENT.format


async def check_client_changeable(client_id: UUID, self_id: UUID) -> None:
    client = await database.query_client_info(client_id=client_id)

    if client is None:
        raise NotFound(can_not_find_client(client_id))

    if client.creator_id != self_id:
        raise Forbidden(inaccessible_client(client_id))


async def check_client_changeable_dependency(
    client_id: UUID, context: TwoFactorTokenDependency
) -> None:
    await check_client_changeable(client_id, context.user_id)
