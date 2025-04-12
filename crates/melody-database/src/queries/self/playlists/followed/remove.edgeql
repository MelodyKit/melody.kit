update global self
set {
    followed_playlists -= (select Playlist filter .id in array_unpack(<array<uuid>>$ids))
};
