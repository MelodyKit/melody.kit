from typing import List

from attrs import define, field
from typing_extensions import Self

from melody.kit.models.album import Album, AlbumData
from melody.kit.models.artist import Artist, ArtistData
from melody.kit.models.playlist import Playlist, PlaylistData
from melody.kit.models.tracks import Track, TrackData
from melody.kit.models.user import User, UserData
from melody.shared.converter import CONVERTER
from melody.shared.typing import Data


class SearchData(Data):
    albums: List[AlbumData]
    artists: List[ArtistData]
    playlists: List[PlaylistData]
    tracks: List[TrackData]
    users: List[UserData]


@define()
class Search:
    albums: List[Album] = field(factory=list)
    artists: List[Artist] = field(factory=list)
    playlists: List[Playlist] = field(factory=list)
    tracks: List[Track] = field(factory=list)
    users: List[User] = field(factory=list)

    @classmethod
    def from_data(cls, data: SearchData) -> Self:
        return CONVERTER.structure(data, cls)

    def into_data(self) -> SearchData:
        return CONVERTER.unstructure(self)  # type: ignore[no-any-return]
