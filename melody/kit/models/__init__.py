from melody.kit.models.album import (
    Album,
    AlbumData,
    AlbumTracks,
    AlbumTracksData,
)
from melody.kit.models.artist import (
    Artist,
    ArtistAlbums,
    ArtistAlbumsData,
    ArtistData,
    ArtistTracks,
    ArtistTracksData,
)
from melody.kit.models.base import (
    Base,
    BaseData,
)
from melody.kit.models.created_at import (
    CreatedAt,
    CreatedAtData,
)
from melody.kit.models.entity import (
    Entity,
    EntityData,
)
from melody.kit.models.pagination import (
    Pagination,
    PaginationData,
)
from melody.kit.models.playlist import (
    PartialPlaylist,
    PartialPlaylistData,
    Playlist,
    PlaylistData,
    PlaylistTracks,
    PlaylistTracksData,
)
from melody.kit.models.statistics import (
    Statistics,
    StatisticsData,
)
from melody.kit.models.streams import (
    BaseStream,
    BaseStreamData,
    Stream,
    StreamData,
    TrackStream,
    TrackStreamData,
    UserStream,
    UserStreamData,
)
from melody.kit.models.tracks import (
    PartialTrack,
    PartialTrackData,
    PositionTrack,
    PositionTrackData,
    Track,
    TrackData,
)
from melody.kit.models.user import (
    User,
    UserAlbums,
    UserAlbumsData,
    UserArtists,
    UserArtistsData,
    UserData,
    UserFollowedPlaylists,
    UserFollowedPlaylistsData,
    UserFollowers,
    UserFollowersData,
    UserFollowing,
    UserFollowingData,
    UserFriends,
    UserFriendsData,
    UserPlaylists,
    UserPlaylistsData,
    UserStreams,
    UserStreamsData,
    UserTracks,
    UserTracksData,
)
from melody.kit.models.user_info import (
    UserInfo,
    UserInfoData,
)
from melody.kit.models.user_settings import (
    UserSettings,
    UserSettingsData,
)

__all__ = (
    # base
    "Base",
    "BaseData",
    # created at
    "CreatedAt",
    "CreatedAtData",
    # entities
    "Entity",
    "EntityData",
    # partial tracks
    "PartialTrack",
    "PartialTrackData",
    # tracks
    "Track",
    "TrackData",
    # position tracks
    "PositionTrack",
    "PositionTrackData",
    # artists
    "Artist",
    "ArtistData",
    # artist tracks
    "ArtistTracks",
    "ArtistTracksData",
    # artist albums
    "ArtistAlbums",
    "ArtistAlbumsData",
    # albums
    "Album",
    "AlbumData",
    # album tracks
    "AlbumTracks",
    "AlbumTracksData",
    # partial playlists
    "PartialPlaylist",
    "PartialPlaylistData",
    # playlists
    "Playlist",
    "PlaylistData",
    # playlist tracks
    "PlaylistTracks",
    "PlaylistTracksData",
    # users
    "User",
    "UserData",
    # user tracks
    "UserTracks",
    "UserTracksData",
    # user albums
    "UserAlbums",
    "UserAlbumsData",
    # user playlists
    "UserPlaylists",
    "UserPlaylistsData",
    # user artists
    "UserArtists",
    "UserArtistsData",
    # user friends
    "UserFriends",
    "UserFriendsData",
    # user followers
    "UserFollowers",
    "UserFollowersData",
    # user following
    "UserFollowing",
    "UserFollowingData",
    # user streams
    "UserStreams",
    "UserStreamsData",
    # user followed playlists
    "UserFollowedPlaylists",
    "UserFollowedPlaylistsData",
    # user info
    "UserInfo",
    "UserInfoData",
    # user settings
    "UserSettings",
    "UserSettingsData",
    # statistics
    "Statistics",
    "StatisticsData",
    # base streams
    "BaseStream",
    "BaseStreamData",
    # user streams
    "UserStream",
    "UserStreamData",
    # track streams
    "TrackStream",
    "TrackStreamData",
    # streams
    "Stream",
    "StreamData",
    # pagination
    "Pagination",
    "PaginationData",
)
