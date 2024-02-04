from melody.kit.models.album import Album, AlbumData, AlbumTracks, AlbumTracksData
from melody.kit.models.artist import (
    Artist,
    ArtistAlbums,
    ArtistAlbumsData,
    ArtistData,
    ArtistTracks,
    ArtistTracksData,
)
from melody.kit.models.base import Base, BaseData
from melody.kit.models.entity import Entity, EntityData
from melody.kit.models.pagination import Pagination, PaginationData
from melody.kit.models.playlist import (
    Playlist,
    PlaylistData,
    PlaylistTracks,
    PlaylistTracksData,
)
from melody.kit.models.search import (
    Search,
    SearchAlbums,
    SearchAlbumsData,
    SearchArtists,
    SearchArtistsData,
    SearchData,
    SearchPlaylists,
    SearchPlaylistsData,
    SearchTracks,
    SearchTracksData,
    SearchUsers,
    SearchUsersData,
)
from melody.kit.models.statistics import Statistics, StatisticsData
from melody.kit.models.streams import Stream, StreamData
from melody.kit.models.tracked import Tracked, TrackedData
from melody.kit.models.tracks import PositionTrack, PositionTrackData, Track, TrackData
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
from melody.kit.models.user_info import UserInfo, UserInfoData
from melody.kit.models.user_settings import UserSettings, UserSettingsData

__all__ = (
    # base
    "Base",
    "BaseData",
    # tracked
    "Tracked",
    "TrackedData",
    # entities
    "Entity",
    "EntityData",
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
    # streams
    "Stream",
    "StreamData",
    # pagination
    "Pagination",
    "PaginationData",
    # search albums
    "SearchAlbums",
    "SearchAlbumsData",
    # search artists
    "SearchArtists",
    "SearchArtistsData",
    # search playlists
    "SearchPlaylists",
    "SearchPlaylistsData",
    # search tracks
    "SearchTracks",
    "SearchTracksData",
    # search users
    "SearchUsers",
    "SearchUsersData",
    # search results
    "Search",
    "SearchData",
)
