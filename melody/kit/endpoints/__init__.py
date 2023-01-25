from melody.kit.endpoints.albums import get_album, get_album_link, get_album_tracks
from melody.kit.endpoints.artists import get_artist, get_artist_link
from melody.kit.endpoints.authentication import login, logout, register
from melody.kit.endpoints.playlists import get_playlist, get_playlist_link, get_playlist_tracks
from melody.kit.endpoints.tracks import get_track, get_track_link
from melody.kit.endpoints.users import get_self, get_self_link, get_user, get_user_link
from melody.kit.endpoints.verify import verify

__all__ = (
    # albums
    "get_album",
    "get_album_link",
    "get_album_tracks",
    # artists
    "get_artist",
    "get_artist_link",
    # authentication
    "login",
    "logout",
    "register",
    # playlists
    "get_playlist",
    "get_playlist_link",
    "get_playlist_tracks",
    # tracks
    "get_track",
    "get_track_link",
    # users
    "get_self",
    "get_self_link",
    "get_user",
    "get_user_link",
    # verification
    "verify",
)
