from typing import Optional
from uuid import UUID

from typing_aliases import Predicate

from melody.kit.core import database
from melody.kit.errors.playlists import PlaylistInaccessible, PlaylistNotFound
from melody.kit.errors.users import UserNotFound
from melody.kit.models.playlist import Playlist
from melody.kit.privacy.shared import are_friends, get_friends, user_id_from_context
from melody.kit.tokens.dependencies import PlaylistsWriteTokenDependency, TokenDependency

__all__ = (
    "check_playlist_accessible",
    "check_playlist_accessible_dependency",
    "check_playlist_changeable",
    "check_playlist_changeable_dependency",
    "create_partial_playlist_accessible_predicate",
    "create_playlist_accessible_predicate",
)


async def check_playlist_accessible(playlist_id: UUID, self_id: Optional[UUID] = None) -> None:
    playlist_privacy = await database.query_playlist_privacy(playlist_id=playlist_id)

    if playlist_privacy is None:
        raise PlaylistNotFound(playlist_id)

    if self_id is None:
        if not playlist_privacy.is_accessible():
            raise PlaylistInaccessible(playlist_id)

        return

    friends = await are_friends(self_id, playlist_privacy.owner.id)

    if not playlist_privacy.is_accessible_by(self_id, friends):
        raise PlaylistInaccessible(playlist_id)


async def check_playlist_accessible_dependency(playlist_id: UUID, context: TokenDependency) -> None:
    await check_playlist_accessible(playlist_id, user_id_from_context(context))


async def check_playlist_changeable(playlist_id: UUID, self_id: UUID) -> None:
    playlist_privacy = await database.query_playlist_privacy(playlist_id=playlist_id)

    if playlist_privacy is None:
        raise PlaylistNotFound(playlist_id)

    if playlist_privacy.owner.id != self_id:
        raise PlaylistInaccessible(playlist_id)


async def check_playlist_changeable_dependency(
    playlist_id: UUID, context: PlaylistsWriteTokenDependency
) -> None:
    await check_playlist_changeable(playlist_id, context.user_id)


async def create_partial_playlist_accessible_predicate(
    owner_id: UUID, self_id: Optional[UUID] = None
) -> Predicate[Playlist]:
    owner = await database.query_user_privacy(owner_id)

    if owner is None:
        raise UserNotFound(owner_id)

    if self_id is None:

        def predicate(playlist: Playlist) -> bool:
            return playlist.privacy_with(owner).is_accessible()

        return predicate

    friends = await get_friends(self_id)

    if friends is None:
        raise UserNotFound(self_id)

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
        raise UserNotFound(self_id)

    def privacy_predicate(playlist: Playlist) -> bool:
        playlist_privacy = playlist.privacy

        return playlist_privacy.is_accessible_by(self_id, playlist_privacy.owner.id in friends)

    return privacy_predicate
