from melody.kit.endpoints.v1.albums import get_album, get_album_link, get_album_tracks
from melody.kit.endpoints.v1.artists import (
    get_artist,
    get_artist_albums,
    get_artist_link,
    get_artist_tracks,
)
from melody.kit.endpoints.v1.authentication import (
    forgot,
    login,
    logout,
    register,
    reset,
    revoke,
    verify,
)
from melody.kit.endpoints.v1.playlists import (
    change_playlist_image,
    create_playlist,
    delete_playlist,
    follow_playlist,
    get_playlist,
    get_playlist_image,
    get_playlist_link,
    get_playlist_tracks,
    unfollow_playlist,
    update_playlist,
)
from melody.kit.endpoints.v1.self import (
    change_self_image,
    get_self,
    get_self_albums,
    get_self_artists,
    get_self_followers,
    get_self_following,
    get_self_friends,
    get_self_image,
    get_self_link,
    get_self_playlists,
    get_self_streams,
    get_self_tracks,
    remove_self_albums,
    remove_self_artists,
    remove_self_tracks,
    save_self_albums,
    save_self_artists,
    save_self_tracks,
)
from melody.kit.endpoints.v1.statistics import get_statistics
from melody.kit.endpoints.v1.tracks import get_track, get_track_link
from melody.kit.endpoints.v1.users import (
    get_user,
    get_user_albums,
    get_user_artists,
    get_user_image,
    get_user_link,
    get_user_playlists,
    get_user_tracks,
)

__all__ = (
    # tracks
    "get_track",
    "get_track_link",
    # artists
    "get_artist",
    "get_artist_link",
    "get_artist_tracks",
    "get_artist_albums",
    # albums
    "get_album",
    "get_album_link",
    "get_album_tracks",
    # playlists
    "create_playlist",
    "get_playlist",
    "update_playlist",
    "delete_playlist",
    "get_playlist_link",
    "get_playlist_image",
    "change_playlist_image",
    "get_playlist_tracks",
    "follow_playlist",
    "unfollow_playlist",
    # users
    "get_user",
    "get_user_link",
    "get_user_image",
    "get_user_tracks",
    "get_user_artists",
    "get_user_albums",
    "get_user_playlists",
    # self
    "get_self",
    "get_self_link",
    "get_self_image",
    "change_self_image",
    "get_self_tracks",
    "save_self_tracks",
    "remove_self_tracks",
    "get_self_artists",
    "save_self_artists",
    "remove_self_artists",
    "get_self_albums",
    "save_self_albums",
    "remove_self_albums",
    "get_self_playlists",
    "get_self_streams",
    "get_self_friends",
    "get_self_followers",
    "get_self_following",
    # statistics
    "get_statistics",
    # authentication
    "login",
    "logout",
    "revoke",
    "register",
    "verify",
    "reset",
    "forgot",
)