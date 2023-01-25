from typing import Optional
from uuid import UUID

from fastapi import Depends, status
from fastapi.responses import FileResponse
from iters import iter

from melody.kit.constants import ME
from melody.kit.core import database, v1
from melody.kit.dependencies import optional_token_dependency, token_dependency
from melody.kit.enums import URIType
from melody.kit.errors import Error, ErrorCode
from melody.kit.models import (
    Playlist,
    User,
    UserAlbumsData,
    UserArtistsData,
    UserData,
    UserFollowersData,
    UserFollowingData,
    UserFriendsData,
    UserPlaylistsData,
    UserTracksData,
    album_into_data,
    artist_into_data,
    playlist_into_data,
    track_into_data,
    user_into_data,
)
from melody.kit.typing import Predicate
from melody.kit.uri import URI

__all__ = (
    "get_self",
    "get_self_link",
    "get_user",
    "get_user_link",
    "get_user_tracks",
    "get_user_artists",
    "get_user_albums",
    "get_user_playlists",
)

CAN_NOT_FIND_USER = "can not find the user with id `{}`"


@v1.get(f"/users/{ME}")
async def get_self(user_id: UUID = Depends(token_dependency)) -> UserData:
    user = await database.query_user(user_id)

    if user is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return user.into_data()


@v1.get(f"/users/{ME}/link")
async def get_self_link(user_id: UUID = Depends(token_dependency)) -> FileResponse:
    uri = URI(type=URIType.USER, id=user_id)

    path = await uri.create_link()

    return FileResponse(path)


@v1.get(f"/users/{ME}/tracks")
async def get_self_tracks(user_id: UUID = Depends(token_dependency)) -> UserTracksData:
    tracks = await database.query_user_tracks(user_id)

    if tracks is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return iter(tracks).map(track_into_data).list()


@v1.get(f"/users/{ME}/artists")
async def get_self_artists(user_id: UUID = Depends(token_dependency)) -> UserArtistsData:
    artists = await database.query_user_artists(user_id)

    if artists is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return iter(artists).map(artist_into_data).list()


@v1.get(f"/users/{ME}/albums")
async def get_self_albums(user_id: UUID = Depends(token_dependency)) -> UserAlbumsData:
    albums = await database.query_user_albums(user_id)

    if albums is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return iter(albums).map(album_into_data).list()


@v1.get(f"/users/{ME}/playlists")
async def get_self_playlists(user_id: UUID = Depends(token_dependency)) -> UserPlaylistsData:
    playlists = await database.query_user_playlists(user_id)

    if playlists is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return iter(playlists).map(playlist_into_data).list()


@v1.get(f"/users/{ME}/friends")
async def get_self_friends(user_id: UUID = Depends(token_dependency)) -> UserFriendsData:
    friends = await database.query_user_friends(user_id)

    if friends is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return iter(friends).map(user_into_data).list()


@v1.get(f"/users/{ME}/followers")
async def get_self_followers(user_id: UUID = Depends(token_dependency)) -> UserFollowersData:
    followers = await database.query_user_followers(user_id)

    if followers is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return iter(followers).map(user_into_data).list()


@v1.get(f"/users/{ME}/following")
async def get_self_following(user_id: UUID = Depends(token_dependency)) -> UserFollowingData:
    following = await database.query_user_following(user_id)

    if following is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return iter(following).map(user_into_data).list()


@v1.get("/users/{user_id}")
async def get_user(user_id: UUID) -> UserData:
    user = await database.query_user(user_id)

    if user is None:
        raise Error(
            CAN_NOT_FIND_USER.format(user_id), ErrorCode.NOT_FOUND, status.HTTP_404_NOT_FOUND
        )

    return user.into_data()


@v1.get("/users/{user_id}/link")
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


INACCESSIBLE_TRACKS = "the tracks of the user with id `{}` are inaccessible"


@v1.get("/users/{user_id}/tracks")
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


INACCESSIBLE_ARTISTS = "the artists of the user with id `{}` are inaccessible"


@v1.get("/users/{user_id}/artists")
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


INACCESSIBLE_ALBUMS = "the albums of the user with id `{}` are inaccessible"


@v1.get("/users/{user_id}/albums")
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


INACCESSIBLE_PLAYLISTS = "the playlists of the user with id `{}` are inaccessible"


@v1.get("/users/{user_id}/playlists")
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
