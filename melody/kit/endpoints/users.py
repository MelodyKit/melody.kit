from typing import Optional
from uuid import UUID

from fastapi import Depends, status
from fastapi.responses import FileResponse
from iters import iter

from melody.kit.core import database, v1
from melody.kit.dependencies import optional_token_dependency
from melody.kit.enums import URIType
from melody.kit.errors import Error, ErrorCode
from melody.kit.models.album import album_into_data
from melody.kit.models.artist import artist_into_data
from melody.kit.models.playlist import Playlist, playlist_into_data
from melody.kit.models.track import track_into_data
from melody.kit.models.user import (
    User,
    UserAlbumsData,
    UserArtistsData,
    UserData,
    UserPlaylistsData,
    UserTracksData,
)
from melody.kit.tags import ALBUMS, ARTISTS, LINKS, PLAYLISTS, TRACKS, USERS
from melody.kit.typing import Predicate
from melody.kit.uri import URI

__all__ = (
    "get_user",
    "get_user_link",
    "get_user_tracks",
    "get_user_artists",
    "get_user_albums",
    "get_user_playlists",
)

CAN_NOT_FIND_USER = "can not find the user with ID `{}`"


@v1.get(
    "/users/{user_id}",
    tags=[USERS],
    summary="Fetches the user with the given ID.",
)
async def get_user(user_id: UUID) -> UserData:
    user = await database.query_user(user_id)

    if user is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return user.into_data()


@v1.get(
    "/users/{user_id}/link",
    tags=[USERS, LINKS],
    summary="Fetches the user link with the given ID.",
)
async def get_user_link(user_id: UUID) -> FileResponse:
    uri = URI(type=URIType.USER, id=user_id)

    path = await uri.create_link()

    return FileResponse(path)


async def check_accessible(user: User, user_id_option: Optional[UUID]) -> bool:
    user_id = user.id

    if user_id_option is not None:
        if user_id_option == user_id:
            return True

    user_privacy_type = user.privacy_type

    if user_privacy_type.is_private():
        return False

    if user_privacy_type.is_friends():
        return user_id_option is not None and await database.check_friends(user_id, user_id_option)

    return True


INACCESSIBLE_TRACKS = "the tracks of the user with ID `{}` are inaccessible"


@v1.get(
    "/users/{user_id}/tracks",
    tags=[USERS, TRACKS],
    summary="Fetches user tracks by the given ID.",
)
async def get_user_tracks(
    user_id: UUID,
    user_id_option: Optional[UUID] = Depends(optional_token_dependency),
) -> UserTracksData:
    user = await database.query_user(user_id)

    if user is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    if await check_accessible(user, user_id_option):
        tracks = await database.query_user_tracks(user_id)

        if tracks is None:
            raise Error(
                CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
            )

        return iter(tracks).map(track_into_data).list()

    raise Error(INACCESSIBLE_TRACKS.format(user_id), ErrorCode.FORBIDDEN, status.HTTP_403_FORBIDDEN)


INACCESSIBLE_ARTISTS = "the artists of the user with ID `{}` are inaccessible"


@v1.get(
    "/users/{user_id}/artists",
    tags=[USERS, ARTISTS],
    summary="Fetches user artists by the given ID.",
)
async def get_user_artists(
    user_id: UUID,
    user_id_option: Optional[UUID] = Depends(optional_token_dependency),
) -> UserArtistsData:
    user = await database.query_user(user_id)

    if user is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    if await check_accessible(user, user_id_option):
        artists = await database.query_user_artists(user_id)

        if artists is None:
            raise Error(
                CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
            )

        return iter(artists).map(artist_into_data).list()

    raise Error(
        INACCESSIBLE_ARTISTS.format(user_id), ErrorCode.FORBIDDEN, status.HTTP_403_FORBIDDEN
    )


INACCESSIBLE_ALBUMS = "the albums of the user with ID `{}` are inaccessible"


@v1.get(
    "/users/{user_id}/albums",
    tags=[USERS, ALBUMS],
    summary="Fetches user albums by the given ID.",
)
async def get_user_albums(
    user_id: UUID,
    user_id_option: Optional[UUID] = Depends(optional_token_dependency),
) -> UserAlbumsData:
    user = await database.query_user(user_id)

    if user is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    if await check_accessible(user, user_id_option):
        albums = await database.query_user_albums(user_id)

        if albums is None:
            raise Error(
                CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
            )

        return iter(albums).map(album_into_data).list()

    raise Error(INACCESSIBLE_ALBUMS.format(user_id), ErrorCode.FORBIDDEN, status.HTTP_403_FORBIDDEN)


async def create_playlist_predicate(
    user_id: UUID, user_id_option: Optional[UUID]
) -> Predicate[Playlist]:
    if user_id_option is None:
        friends = False

    else:
        friends = await database.check_friends(user_id, user_id_option)

    def predicate(playlist: Playlist) -> bool:
        privacy_type = playlist.privacy_type

        if privacy_type.is_private():
            return False

        if privacy_type.is_friends():
            return friends

        return True

    return predicate


INACCESSIBLE_PLAYLISTS = "the playlists of the user with ID `{}` are inaccessible"


@v1.get(
    "/users/{user_id}/playlists",
    tags=[USERS, PLAYLISTS],
    summary="Fetches user playlists by the given ID.",
)
async def get_user_playlists(
    user_id: UUID,
    user_id_option: Optional[UUID] = Depends(optional_token_dependency),
) -> UserPlaylistsData:
    user = await database.query_user(user_id)

    if user is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    if await check_accessible(user, user_id_option):
        playlists = await database.query_user_playlists(user_id)

        if playlists is None:
            raise Error(
                CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
            )

        return (
            iter(playlists)
            .filter(await create_playlist_predicate(user_id, user_id_option))
            .map(playlist_into_data)
            .list()
        )

    raise Error(
        INACCESSIBLE_PLAYLISTS.format(user_id), ErrorCode.FORBIDDEN, status.HTTP_403_FORBIDDEN
    )
