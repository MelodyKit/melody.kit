from melody.kit.endpoints.albums import get_album, get_album_link, get_album_tracks
from melody.kit.endpoints.artists import (
    get_artist,
    get_artist_albums,
    get_artist_link,
    get_artist_tracks,
)
from melody.kit.endpoints.authentication import login, register, revoke, verify
from melody.kit.endpoints.playlists import get_playlist, get_playlist_link, get_playlist_tracks
from melody.kit.endpoints.self import (
    get_self,
    get_self_albums,
    get_self_artists,
    get_self_followers,
    get_self_following,
    get_self_friends,
    get_self_link,
    get_self_playlists,
    get_self_streams,
    get_self_tracks,
)
from melody.kit.endpoints.statistics import get_statistics
from melody.kit.endpoints.tracks import get_track, get_track_link
from melody.kit.endpoints.users import (
    get_user,
    get_user_albums,
    get_user_artists,
    get_user_link,
    get_user_playlists,
    get_user_tracks,
)

__all__ = (
    # albums
    "get_album",
    "get_album_link",
    "get_album_tracks",
    # artists
    "get_artist",
    "get_artist_link",
    "get_artist_tracks",
    "get_artist_albums",
    # authentication
    "login",
    "revoke",
    "register",
    "verify",
    # playlists
    "get_playlist",
    "get_playlist_link",
    "get_playlist_tracks",
    # tracks
    "get_track",
    "get_track_link",
    # users
    "get_user",
    "get_user_link",
    "get_user_tracks",
    "get_user_artists",
    "get_user_albums",
    "get_user_playlists",
    # self
    "get_self",
    "get_self_link",
    "get_self_tracks",
    "get_self_artists",
    "get_self_albums",
    "get_self_playlists",
    "get_self_streams",
    "get_self_friends",
    "get_self_followers",
    "get_self_following",
    # statistics
    "get_statistics",
)
